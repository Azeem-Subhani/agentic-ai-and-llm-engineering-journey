"""
Ingest Markdown files from ``knowledge-base/`` into a Chroma vector store.

This is the **baseline** pipeline: LangChain loaders, fixed-size chunking with
overlap, and OpenAI embeddings. Run from the ``rag-system`` directory::

    python -m implementation.ingest
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Paths & hyperparameters (tune chunking for your corpus)
# ---------------------------------------------------------------------------

RAG_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = RAG_ROOT / "knowledge-base"
VECTOR_DB_DIR = os.environ.get("INSURELLM_VECTOR_DB", str(RAG_ROOT / "vector_db"))

CHUNK_SIZE = 500
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-large"

load_dotenv(override=True)
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)


def fetch_documents():
    """
    Load every ``*.md`` file under ``knowledge-base/<category>/``.

    Each document's metadata includes ``doc_type`` (folder name: company,
    products, contracts, employees).
    """
    folders = glob.glob(str(KNOWLEDGE_BASE_DIR / "*"))
    documents: list = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(
            folder,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    return documents


def create_chunks(documents):
    """Split documents into overlapping text chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def create_embeddings(chunks):
    """
    Persist chunks to Chroma. Deletes any existing collection at ``VECTOR_DB_DIR``
    first so re-ingestion starts fresh.
    """
    if os.path.exists(VECTOR_DB_DIR):
        Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR,
    )

    collection = vectorstore._collection
    count = collection.count()
    sample = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")
    return vectorstore


def main():
    documents = fetch_documents()
    print(f"Loaded {len(documents)} source documents")
    chunks = create_chunks(documents)
    print(f"Created {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    create_embeddings(chunks)
    print("Ingestion complete")


if __name__ == "__main__":
    main()
