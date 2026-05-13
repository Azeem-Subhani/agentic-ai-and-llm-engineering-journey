"""
Day 2 style demo: chunk documents, embed with a small local model, print stats.

Optional: 2D t-SNE scatter (requires scikit-learn + matplotlib). Install::

    pip install scikit-learn matplotlib

Run::

    python examples/02_embeddings_and_visualization.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    load_dotenv(override=True)
    kb = ROOT / "knowledge-base"
    print(f"Loading Markdown from: {kb}")

    loader = DirectoryLoader(
        str(kb),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} raw documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    print(f"Embedding model: {EMBED_MODEL}")

    vs = Chroma.from_documents(documents=chunks, embedding=embeddings)
    sample = vs._collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dim = len(sample)
    preview = [round(x, 4) for x in sample[:8]]
    print(f"Each chunk vector has dimension {dim}")
    print(f"First 8 values of one vector: {preview}")

    try:
        import numpy as np
        from sklearn.manifold import TSNE
        import matplotlib.pyplot as plt

        n = min(80, len(chunks))
        texts = [c.page_content[:80].replace("\n", " ") for c in chunks[:n]]
        vectors = embeddings.embed_documents([c.page_content for c in chunks[:n]])
        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, n - 1))
        reduced = tsne.fit_transform(np.array(vectors))
        out = ROOT / "examples" / "_tsne_demo.png"
        plt.figure(figsize=(8, 6))
        plt.scatter(reduced[:, 0], reduced[:, 1], alpha=0.7)
        plt.title("t-SNE of chunk embeddings (subset)")
        plt.xlabel("dim 1")
        plt.ylabel("dim 2")
        plt.tight_layout()
        plt.savefig(out, dpi=120)
        print(f"Saved t-SNE plot to: {out}")
    except ImportError:
        print("Optional: pip install scikit-learn matplotlib numpy to write _tsne_demo.png")


if __name__ == "__main__":
    main()
