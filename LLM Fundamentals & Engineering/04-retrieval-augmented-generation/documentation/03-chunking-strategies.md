# 03 — Chunking strategies

## What this guide is about

**Chunking** means splitting long documents into smaller pieces that fit in the context window and match the granularity of user questions. You will see **fixed-size** chunking (baseline) and **LLM-authored** chunks (advanced).

## Why chunk at all?

Retrieval returns **whole chunks**. If a chunk is huge, it dilutes signal: the embedding averages over many topics. If a chunk is tiny, it may miss necessary context. Chunking is the dial you turn first.

## Fixed-size chunking (baseline)

[`rag-system/implementation/ingest.py`](../rag-system/implementation/ingest.py) uses LangChain’s `RecursiveCharacterTextSplitter` with:

- `CHUNK_SIZE = 500` characters (not tokens — close enough for teaching),
- `CHUNK_OVERLAP = 200` characters.

Overlap means the **end of one chunk repeats at the start of the next** so a sentence sitting on a boundary still appears in full in at least one chunk.

### Minimal splitting example

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "A" * 600  # pretend long text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
parts = splitter.split_text(text)
print("num_parts", len(parts))
print("len0", len(parts[0]), "len1", len(parts[1]))
```

**Example output:**

```text
num_parts 2
len0 500 len1 300
```

What this output tells you: overlap forces **extra** chunks when content is longer than one window — boundaries are soft, not hard page breaks.

## Run baseline ingest to see real counts

```bash
cd rag-system
python -m implementation.ingest
```

**Example output:**

```text
Loaded 76 source documents
Created 432 chunks (size=500, overlap=200)
There are 432 vectors with 3,072 dimensions in the vector store
Ingestion complete
```

What this output tells you: **76** Markdown files became **432** overlapping training units for retrieval.

## LLM chunking (advanced)

[`rag-system/pro_implementation/ingest.py`](../rag-system/pro_implementation/ingest.py) sends each **full document** to an LLM and asks for structured pieces:

- `headline` — short surface form users might query,
- `summary` — paraphrase for retrieval,
- `original_text` — verbatim excerpt.

Those three fields are concatenated into `page_content` before embedding. This can improve retrieval when headings and summaries **align with user phrasing**.

```bash
cd rag-system
python -m pro_implementation.ingest
```

**Example output:**

```text
Loaded 76 documents
100%|██████████| 76/76 [12:34<00:00,  9.87s/it]
Total chunks after LLM preprocessing: 512
Vectorstore created with 512 documents
Ingestion complete
```

What this output tells you: advanced ingest is **slower and costlier** (one LLM call per source file, plus embeddings) but can yield **richer** retrieval units.

## Tradeoffs (quick table)

| Approach | Pros | Cons |
|----------|------|------|
| Fixed splitter | Fast, cheap, deterministic | Blind to document semantics |
| LLM chunking | Chunks aligned to questions | API cost, variability, needs QA |

## What to remember

- Chunk size controls **retrieval granularity**; overlap protects **boundary cuts**.
- Baseline = **RecursiveCharacterTextSplitter**; advanced = **LLM-structured chunks**.

Next: [`04-retrieval-pipelines-and-similarity-search.md`](04-retrieval-pipelines-and-similarity-search.md)
