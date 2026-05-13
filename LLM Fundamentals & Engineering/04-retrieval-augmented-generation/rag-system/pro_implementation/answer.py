"""
**Advanced RAG**: query rewriting, dual-query dense retrieval, LLM reranking, then
answer generation via LiteLLM.

Requires a populated ``preprocessed_db`` (see ``pro_implementation.ingest``).
Default completion model is OpenAI through LiteLLM; override with env
``INSURELLM_PRO_CHAT_MODEL``.
"""

from __future__ import annotations

import os
from pathlib import Path

from chromadb import PersistentClient
from dotenv import load_dotenv
from litellm import completion
from openai import OpenAI
from pydantic import BaseModel, Field
from tenacity import retry, wait_exponential

RAG_ROOT = Path(__file__).resolve().parent.parent
DB_NAME = os.environ.get("INSURELLM_PREPROCESSED_DB", str(RAG_ROOT / "preprocessed_db"))

COLLECTION_NAME = "docs"
EMBEDDING_MODEL = "text-embedding-3-large"
# Valid LiteLLM route (OpenAI). For Groq: ``groq/llama-3.3-70b-versatile`` etc.
CHAT_MODEL = os.environ.get("INSURELLM_PRO_CHAT_MODEL", "openai/gpt-4.1-nano")

RETRIEVAL_K = 20
FINAL_K = 10

WAIT = wait_exponential(multiplier=1, min=10, max=240)

load_dotenv(override=True)
openai_client = OpenAI()
chroma = PersistentClient(path=DB_NAME)
collection = chroma.get_or_create_collection(COLLECTION_NAME)

SYSTEM_PROMPT = """You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
Your answer will be evaluated for accuracy, relevance and completeness, so make sure it only answers the question and fully answers it.
If you don't know the answer, say so.
For context, here are specific extracts from the Knowledge Base that might be directly relevant to the user's question:
{context}

With this context, please answer the user's question. Be accurate, relevant and complete.
"""


class Result(BaseModel):
    page_content: str
    metadata: dict


class RankOrder(BaseModel):
    order: list[int] = Field(
        description="The order of relevance of chunks, from most relevant to least relevant, by chunk id number"
    )


@retry(wait=WAIT)
def rerank(question: str, chunks: list[Result]) -> list[Result]:
    system_prompt = """
You are a document re-ranker.
You are provided with a question and a list of relevant chunks of text from a query of a knowledge base.
The chunks are provided in the order they were retrieved; this should be approximately ordered by relevance, but you may be able to improve on that.
You must rank order the provided chunks by relevance to the question, with the most relevant chunk first.
Reply only with the list of ranked chunk ids, nothing else. Include all the chunk ids you are provided with, reranked.
"""
    user_prompt = (
        f"The user has asked the following question:\n\n{question}\n\n"
        "Order all the chunks of text by relevance to the question, from most relevant to least relevant. "
        "Include all the chunk ids you are provided with, reranked.\n\nHere are the chunks:\n\n"
    )
    for index, chunk in enumerate(chunks):
        user_prompt += f"# CHUNK ID: {index + 1}:\n\n{chunk.page_content}\n\n"
    user_prompt += "Reply only with the list of ranked chunk ids, nothing else."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = completion(model=CHAT_MODEL, messages=messages, response_format=RankOrder)
    reply = response.choices[0].message.content
    order = RankOrder.model_validate_json(reply).order
    return [chunks[i - 1] for i in order]


def make_rag_messages(question: str, history: list, chunks: list[Result]):
    context = "\n\n".join(
        f"Extract from {chunk.metadata['source']}:\n{chunk.page_content}" for chunk in chunks
    )
    system_prompt = SYSTEM_PROMPT.format(context=context)
    return [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": question}]


@retry(wait=WAIT)
def rewrite_query(question: str, history: list | None = None) -> str:
    """Produce a short KB search query optimized for dense retrieval."""
    history = history or []
    message = f"""
You are in a conversation with a user, answering questions about the company Insurellm.
You are about to look up information in a Knowledge Base to answer the user's question.

This is the history of your conversation so far with the user:
{history}

And this is the user's current question:
{question}

Respond only with a short, refined question that you will use to search the Knowledge Base.
It should be a VERY short specific question most likely to surface content. Focus on the question details.
IMPORTANT: Respond ONLY with the precise knowledgebase query, nothing else.
"""
    response = completion(model=CHAT_MODEL, messages=[{"role": "system", "content": message}])
    return response.choices[0].message.content


def merge_chunks(chunks: list[Result], reranked: list[Result]) -> list[Result]:
    """Union two retrieval lists without duplicate page_content."""
    merged = chunks[:]
    existing = [chunk.page_content for chunk in chunks]
    for chunk in reranked:
        if chunk.page_content not in existing:
            merged.append(chunk)
            existing.append(chunk.page_content)
    return merged


def fetch_context_unranked(question: str) -> list[Result]:
    query = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=[question]).data[0].embedding
    results = collection.query(query_embeddings=[query], n_results=RETRIEVAL_K)
    chunks: list[Result] = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(Result(page_content=doc, metadata=meta))
    return chunks


def fetch_context(original_question: str) -> list[Result]:
    """
    Dual-query retrieval (original + rewritten), merge, rerank, keep top ``FINAL_K``.
    """
    rewritten_question = rewrite_query(original_question)
    chunks1 = fetch_context_unranked(original_question)
    chunks2 = fetch_context_unranked(rewritten_question)
    chunks = merge_chunks(chunks1, chunks2)
    reranked = rerank(original_question, chunks)
    return reranked[:FINAL_K]


@retry(wait=WAIT)
def answer_question(question: str, history: list | None = None) -> tuple[str, list[Result]]:
    """Return (answer text, final reranked chunks shown to the model)."""
    history = history or []
    chunks = fetch_context(question)
    messages = make_rag_messages(question, history, chunks)
    response = completion(model=CHAT_MODEL, messages=messages)
    return response.choices[0].message.content, chunks
