"""
Baseline RAG answering: Chroma retrieval + OpenAI chat with a system prompt.

Retrieval uses the LangChain retriever with a fixed ``k``. Conversation history
is flattened into one string for retrieval only; the model still receives the
structured message list for generation.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, convert_to_messages
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

RAG_ROOT = Path(__file__).resolve().parent.parent
DB_NAME = os.environ.get("INSURELLM_VECTOR_DB", str(RAG_ROOT / "vector_db"))

CHAT_MODEL = "gpt-4.1-nano"
EMBEDDING_MODEL = "text-embedding-3-large"
RETRIEVAL_K = 10

SYSTEM_PROMPT = """You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

load_dotenv(override=True)

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})
llm = ChatOpenAI(temperature=0, model_name=CHAT_MODEL)


def fetch_context(question: str) -> list[Document]:
    """Return the top-``RETRIEVAL_K`` chunks most similar to ``question``."""
    return retriever.invoke(question)


def combined_question(question: str, history: list[dict] | None = None) -> str:
    """
    Build a single retrieval query from prior user turns plus the latest question.

    This helps multi-turn chats surface documents that match the full thread,
    not only the last utterance.
    """
    history = history or []
    prior = "\n".join(m["content"] for m in history if m.get("role") == "user")
    return (prior + "\n" + question).strip()


def answer_question(
    question: str,
    history: list[dict] | None = None,
) -> tuple[str, list[Document]]:
    """
    Run retrieval on the combined user thread, then answer with ``CHAT_MODEL``.

    Returns:
        Tuple of (assistant reply text, retrieved ``Document`` list).
    """
    history = history or []
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content, docs
