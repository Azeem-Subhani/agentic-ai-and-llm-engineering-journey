# 01 — What is RAG and why it exists

## What this guide is about

You will learn what **Retrieval-Augmented Generation (RAG)** means in plain language, why teams build it, and how a **very simple** “lookup” system already shows the core idea (even before vectors).

## Why plain LLMs are risky for company Q&A

A large language model is trained on **public text up to a cutoff date**. It does **not** automatically know:

- your private contracts,
- this quarter’s headcount,
- which employee won an internal award last year.

When it still answers confidently, that is often a **hallucination**: fluent language that is **not** grounded in real facts.

### Tiny experiment: model without your documents

Imagine asking: “How many employees does Insurellm currently have?” If the model has **no** access to your internal `overview.md`, it might guess or refuse. With **no retrieval**, you cannot tell from the API alone whether it “knows” or is guessing.

```python
# Pseudocode — illustrates the risk, not the Insurellm repo
question = "How many employees does Insurellm currently have?"
# If you send only the question with no internal context, the model may hallucinate or hedge.
print("Without retrieval, the model must rely on memorized / guessed world knowledge.")
```

**Example output:**

```text
Without retrieval, the model must rely on memorized / guessed world knowledge.
```

What this output tells you: we are highlighting that **the model alone** does not have a trustworthy link to **your** files.

## Context limits (why you cannot paste everything)

Even if you wanted to paste all Markdown files into one prompt, models have a **context window** (a maximum number of tokens they can read at once). Your knowledge base can be **larger** than that window. RAG solves this by **choosing a small relevant slice** at query time.

## What RAG adds

**RAG** means:

1. **Retrieve** a few pieces of text that are likely relevant to the user’s question.
2. **Augment** the prompt (prepend those pieces as “evidence”).
3. **Generate** an answer that cites or follows that evidence.

Analogy: a **closed-book exam** vs an **open-book exam**. RAG is the open-book version: the model still reasons, but it reads selected pages first.

## Business story: Insurellm “expert assistant”

Insurellm employees need accurate answers about products, contracts, and people. A single wrong number in a contract answer can be expensive. RAG targets:

- **Accuracy** (ground answers in retrieved text),
- **Freshness** (re-ingest Markdown when files change),
- **Cost control** (smaller context than sending everything).

## Day-1 style baseline: keyword overlap (no vectors yet)

The script [`rag-system/examples/01_keyword_retrieval_demo.py`](../rag-system/examples/01_keyword_retrieval_demo.py) loads employee and product Markdown into Python dictionaries and scores overlap between **question words** and **document words**.

```bash
cd rag-system
python examples/01_keyword_retrieval_demo.py
```

**Example output:**

```text
Question: Who won the IIOTY award in 2023?

--- Retrieved context (keyword overlap) ---

[Matched bucket: thompson | overlap score: 12]

# Maxine Thompson
...
(employee profile text appears here)

--- ... (truncated if long) ---

Model answer:
 Maxine Thompson won the Insurellm Innovator of the Year (IIOTY) award in 2023.
```

What this output tells you: even **dumb** retrieval (counting shared words) can sometimes pull the right profile — but it breaks when users paraphrase, use synonyms, or ask cross-document questions. That motivates **semantic search** with embeddings (guide 02).

## What to remember

- **Hallucination** is fluent but unsupported content; RAG reduces it by supplying **evidence** first.
- **Context windows** force you to retrieve a **subset** of documents, not the whole library.
- A **keyword** retriever is a teaching stepping stone; real systems usually use **embeddings** (next guides).

Next: [`02-embeddings-and-vector-databases.md`](02-embeddings-and-vector-databases.md)
