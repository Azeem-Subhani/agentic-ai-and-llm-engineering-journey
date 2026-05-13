# Documentation index — Module 04 (RAG)

## Who this is for

Readers who can run small Python programs but **do not** need prior experience with embeddings, vector databases, or information retrieval. Each guide introduces terms in plain language and pairs code with **example output** so you can follow along without executing every snippet.

## Prerequisites

- Python environment set up as in the module [`README.md`](../README.md).
- Optional but recommended: complete **Module 01** (LLM fundamentals), **Module 02** (models and tokenizers), **Module 03** (evaluation mindset).

## Best reading order

1. [`01-what-is-rag-and-why-it-exists.md`](01-what-is-rag-and-why-it-exists.md)
2. [`02-embeddings-and-vector-databases.md`](02-embeddings-and-vector-databases.md)
3. [`03-chunking-strategies.md`](03-chunking-strategies.md)
4. [`04-retrieval-pipelines-and-similarity-search.md`](04-retrieval-pipelines-and-similarity-search.md)
5. [`05-building-the-basic-rag-pipeline.md`](05-building-the-basic-rag-pipeline.md)
6. [`06-advanced-rag-query-rewriting-and-reranking.md`](06-advanced-rag-query-rewriting-and-reranking.md)
7. [`07-evaluating-rag-systems.md`](07-evaluating-rag-systems.md)
8. [`08-llm-as-a-judge.md`](08-llm-as-a-judge.md)
9. [`09-the-gradio-applications.md`](09-the-gradio-applications.md)
10. [`10-production-considerations-and-tradeoffs.md`](10-production-considerations-and-tradeoffs.md)

## How the code is organized

| Folder under `rag-system/` | Purpose |
|----------------------------|---------|
| `implementation/` | **Baseline** LangChain + Chroma + OpenAI ingest and answer. Used by `app.py` and `evaluation/eval.py`. |
| `pro_implementation/` | **Advanced** LLM chunking, native Chroma, query rewrite, dual retrieval, rerank, LiteLLM answers. |
| `evaluation/` | JSONL test suite + retrieval metrics + judge prompts. |
| `examples/` | Small runnable demos aligned with the learning path. |
| `knowledge-base/` | Synthetic Insurellm Markdown (do not edit for coursework). |

## Glossary (quick)

| Term | One-line meaning |
|------|------------------|
| **RAG** | Retrieve text from a knowledge base, then generate an answer that is grounded in that text. |
| **Embedding** | A fixed-length list of numbers representing text so that “similar meaning” is “close” in vector space. |
| **Chunk** | A slice of a document used as the unit of retrieval. |
| **Vector database** | Storage + search for embeddings (here: Chroma). |
| **Retriever** | The component that turns a question into top-*k* chunks. |
| **Reranking** | A second step that re-orders candidate chunks for relevance. |
| **LLM-as-judge** | Using an LLM to score another model’s answer against a reference. |
| **MRR / nDCG** | Retrieval metrics used in this module’s harness (explained in guide 07). |

## Goal of this module

By the end you should be able to explain **end-to-end RAG**, run the **baseline** system, interpret **evaluation** results, and reason about **when** to adopt advanced patterns.

Next: [`01-what-is-rag-and-why-it-exists.md`](01-what-is-rag-and-why-it-exists.md)
