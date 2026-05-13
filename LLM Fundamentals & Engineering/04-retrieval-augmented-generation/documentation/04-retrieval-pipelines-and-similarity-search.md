# 04 — Retrieval pipelines and similarity search

## What this guide is about

How a question becomes **top-k** evidence chunks: embed the question, compare vectors, return the closest chunks. You will also see how **chat history** changes the retrieval query string in this codebase.

## Similarity search in one sentence

The database returns chunks whose embedding vectors have **high cosine similarity** with the question embedding — “pointing roughly the same direction” in high-dimensional space.

## k-nearest neighbors (kNN)

**k** is simply “how many chunks to fetch.” In [`implementation/answer.py`](../rag-system/implementation/answer.py), `RETRIEVAL_K = 10` and the retriever is built with:

> **Prerequisite:** run `python -m implementation.ingest` once so `vector_db/` exists; commands below assume `cd rag-system`.

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})
```

At query time:

```python
docs = retriever.invoke("How many employees does Insurellm have?")
print("retrieved", len(docs))
print("first source:", docs[0].metadata.get("source"))
print("preview:", docs[0].page_content[:120].replace("\n", " "))
```

**Example output:**

```text
retrieved 10
first source: .../knowledge-base/company/overview.md
preview: # Insurellm Overview Insurellm is an insurance technology company ...
```

What this output tells you: the vector store returned **10** chunks; the top one is from the **company** folder — sensible for a headcount question.

## Multi-turn retrieval: `combined_question`

Users rarely ask one isolated sentence. The baseline pipeline **concatenates prior user utterances** before retrieval so the embedding reflects the whole thread:

```python
from implementation.answer import combined_question

history = [
    {"role": "user", "content": "Tell me about our products."},
    {"role": "assistant", "content": "We offer several product lines..."},
]
q = "Which one is for auto insurers?"
print(combined_question(q, history))
```

**Example output:**

```text
Tell me about our products.
Which one is for auto insurers?
```

What this output tells you: retrieval sees **both** lines, which helps disambiguate “which one” to **Carllm**-style content.

## Dense vs sparse (orientation only)

- **Dense** retrieval = embeddings (what this module uses).
- **Sparse** retrieval = keyword indexes (BM25). Hybrid systems combine both; this course focuses on dense for clarity.

## What to remember

- **Top-k** retrieval is approximate nearest neighbor search in embedding space.
- **History flattening** (`combined_question`) improves retrieval for follow-ups.

Next: [`05-building-the-basic-rag-pipeline.md`](05-building-the-basic-rag-pipeline.md)
