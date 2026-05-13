"""
**Advanced ingest**: LLM-authored chunks (headline + summary + verbatim text) stored
in Chroma via the native client and batched OpenAI embeddings.

Uses LiteLLM for the structuring model so you can swap providers with one string.
Run from ``rag-system``::

    python -m pro_implementation.ingest
"""

from __future__ import annotations

import os
from multiprocessing import Pool
from pathlib import Path

from chromadb import PersistentClient
from dotenv import load_dotenv
from litellm import completion
from openai import OpenAI
from pydantic import BaseModel, Field
from tenacity import retry, wait_exponential
from tqdm import tqdm

RAG_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_PATH = RAG_ROOT / "knowledge-base"
DB_NAME = os.environ.get("INSURELLM_PREPROCESSED_DB", str(RAG_ROOT / "preprocessed_db"))

# LiteLLM model id (OpenAI by default; set GROQ_API_KEY etc. if you change provider)
CHUNKING_MODEL = os.environ.get("INSURELLM_CHUNK_MODEL", "openai/gpt-4.1-nano")
EMBEDDING_MODEL = "text-embedding-3-large"
COLLECTION_NAME = "docs"

# Target minimum chunk count hint for the LLM (not a hard limit)
AVERAGE_CHUNK_SIZE = 100
WORKERS = int(os.environ.get("INSURELLM_INGEST_WORKERS", "3"))

WAIT = wait_exponential(multiplier=1, min=10, max=240)

load_dotenv(override=True)
openai_client = OpenAI()


class Result(BaseModel):
    page_content: str
    metadata: dict


class Chunk(BaseModel):
    headline: str = Field(
        description="A brief heading for this chunk, typically a few words, that is most likely to be surfaced in a query",
    )
    summary: str = Field(
        description="A few sentences summarizing the content of this chunk to answer common questions"
    )
    original_text: str = Field(
        description="The original text of this chunk from the provided document, exactly as is, not changed in any way"
    )

    def as_result(self, document: dict) -> Result:
        metadata = {"source": document["source"], "type": document["type"]}
        return Result(
            page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata,
        )


class Chunks(BaseModel):
    chunks: list[Chunk]


def fetch_documents():
    """Walk ``knowledge-base`` and return one dict per Markdown file."""
    documents = []
    for folder in KNOWLEDGE_BASE_PATH.iterdir():
        if not folder.is_dir():
            continue
        doc_type = folder.name
        for file in folder.rglob("*.md"):
            with open(file, "r", encoding="utf-8") as f:
                documents.append({"type": doc_type, "source": file.as_posix(), "text": f.read()})

    print(f"Loaded {len(documents)} documents")
    return documents


def make_prompt(document: dict) -> str:
    how_many = (len(document["text"]) // AVERAGE_CHUNK_SIZE) + 1
    return f"""
You take a document and you split the document into overlapping chunks for a KnowledgeBase.

The document is from the shared drive of a company called Insurellm.
The document is of type: {document["type"]}
The document has been retrieved from: {document["source"]}

A chatbot will use these chunks to answer questions about the company.
You should divide up the document as you see fit, being sure that the entire document is returned across the chunks - don't leave anything out.
This document should probably be split into at least {how_many} chunks, but you can have more or less as appropriate, ensuring that there are individual chunks to answer specific questions.
There should be overlap between the chunks as appropriate; typically about 25% overlap or about 50 words, so you have the same text in multiple chunks for best retrieval results.

For each chunk, you should provide a headline, a summary, and the original text of the chunk.
Together your chunks should represent the entire document with overlap.

Here is the document:

{document["text"]}

Respond with the chunks.
"""


def make_messages(document: dict):
    return [{"role": "user", "content": make_prompt(document)}]


@retry(wait=WAIT)
def process_document(document: dict) -> list[Result]:
    response = completion(
        model=CHUNKING_MODEL,
        messages=make_messages(document),
        response_format=Chunks,
    )
    reply = response.choices[0].message.content
    doc_as_chunks = Chunks.model_validate_json(reply).chunks
    return [chunk.as_result(document) for chunk in doc_as_chunks]


def create_chunks(documents):
    """
    Parallel LLM chunking. If you hit rate limits, set env ``INSURELLM_INGEST_WORKERS=1``.
    """
    chunks: list[Result] = []
    with Pool(processes=WORKERS) as pool:
        for result in tqdm(pool.imap_unordered(process_document, documents), total=len(documents)):
            chunks.extend(result)
    return chunks


def create_embeddings(chunks: list[Result]):
    chroma = PersistentClient(path=DB_NAME)
    if COLLECTION_NAME in [c.name for c in chroma.list_collections()]:
        chroma.delete_collection(COLLECTION_NAME)

    texts = [chunk.page_content for chunk in chunks]
    emb = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=texts).data
    vectors = [e.embedding for e in emb]

    collection = chroma.get_or_create_collection(COLLECTION_NAME)
    ids = [str(i) for i in range(len(chunks))]
    metas = [chunk.metadata for chunk in chunks]
    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
    print(f"Vectorstore created with {collection.count()} documents")


def main():
    documents = fetch_documents()
    chunks = create_chunks(documents)
    print(f"Total chunks after LLM preprocessing: {len(chunks)}")
    create_embeddings(chunks)
    print("Ingestion complete")


if __name__ == "__main__":
    main()
