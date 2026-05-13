# Module 04 — Retrieval-Augmented Generation (RAG)

This module teaches **Retrieval-Augmented Generation** from first principles: why plain LLMs are not enough, how embeddings and vector search work, how to build ingest + query pipelines, how to evaluate retrieval and answers, and what changes in a more “production-shaped” advanced stack.

You work with a fictional company, **Insurellm**, and a structured **knowledge base** of Markdown files (company, products, contracts, employees). The runnable code lives under [`rag-system/`](rag-system/).

## What you will learn

- Why organizations add **retrieval** on top of an LLM (accuracy, freshness, control).
- **Embeddings**, **chunking**, **vector databases**, and **similarity search**.
- A **baseline RAG** path (LangChain + Chroma + OpenAI) used by the chat app and the evaluation harness.
- An **advanced RAG** path (LLM chunking, query rewriting, dual retrieval, LLM reranking) in `pro_implementation/`.
- **Evaluation**: keyword-based retrieval metrics and **LLM-as-a-judge** for answers.
- **Tradeoffs** you hit when moving toward production (cost, latency, monitoring).

## Repository layout

| Path | Role |
|------|------|
| [`documentation/`](documentation/) | Course-style Markdown guides (start in `documentation/README.md`). |
| [`rag-system/implementation/`](rag-system/implementation/) | Baseline ingest + answer (`ingest.py`, `answer.py`). |
| [`rag-system/pro_implementation/`](rag-system/pro_implementation/) | Advanced ingest + answer. |
| [`rag-system/evaluation/`](rag-system/evaluation/) | `tests.jsonl` suite, `eval.py`, `test.py`. |
| [`rag-system/examples/`](rag-system/examples/) | Small scripts that replace the old day-by-day notebooks. |
| [`rag-system/knowledge-base/`](rag-system/knowledge-base/) | **Read-only** synthetic Markdown corpus. |
| [`rag-system/app.py`](rag-system/app.py) | Gradio chat UI. |
| [`rag-system/evaluator.py`](rag-system/evaluator.py) | Gradio evaluation dashboard. |

## Prerequisites

- Python **3.10+** recommended.
- Modules **01–03** in this course (LLM basics, open models, selection/eval mindset) — not strictly required but helpful.
- An **OpenAI API key** for embeddings and chat (`OPENAI_API_KEY` in a `.env` file inside `rag-system/` or your shell environment).

## Setup

```bash
cd "LLM Fundamentals & Engineering/04-retrieval-augmented-generation"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `rag-system/.env`:

```text
OPENAI_API_KEY=sk-...
```

## Typical workflow (baseline)

All commands assume your shell is in **`rag-system/`**:

```bash
cd rag-system
python -m implementation.ingest
python app.py
```

**Example output** from ingest (numbers depend on corpus size):

```text
Loaded 76 source documents
Created 432 chunks (size=500, overlap=200)
There are 432 vectors with 3,072 dimensions in the vector store
Ingestion complete
```

## Evaluation CLI

```bash
cd rag-system
python evaluation/eval.py 0
```

This prints retrieval metrics and runs one full **answer + judge** cycle for test row `0`.

## Progressive examples

| Script | Idea |
|--------|------|
| [`examples/01_keyword_retrieval_demo.py`](rag-system/examples/01_keyword_retrieval_demo.py) | Keyword overlap “retrieval” without vectors. |
| [`examples/02_embeddings_and_visualization.py`](rag-system/examples/02_embeddings_and_visualization.py) | Chunk + embed + optional t-SNE plot. |
| [`examples/03_basic_rag_demo.py`](rag-system/examples/03_basic_rag_demo.py) | One question through `answer_question`. |
| [`examples/04_evaluation_demo.py`](rag-system/examples/04_evaluation_demo.py) | Load `tests.jsonl` and print retrieval metrics for row 0. |
| [`examples/05_advanced_rag_demo.py`](rag-system/examples/05_advanced_rag_demo.py) | Advanced stack (needs `preprocessed_db`). |

## Reading order

Open **[`documentation/README.md`](documentation/README.md)** for the numbered reading path, glossary, and how each guide maps to code.

## What to remember

- **RAG** = retrieve trustworthy text, then let the LLM **read** it while answering.
- The **baseline** stack is what the shipped **eval harness** measures by default.
- The **advanced** stack is a second architecture to study; wiring it into `evaluation/eval.py` is left as an optional exercise.

Next: [`documentation/README.md`](documentation/README.md)
