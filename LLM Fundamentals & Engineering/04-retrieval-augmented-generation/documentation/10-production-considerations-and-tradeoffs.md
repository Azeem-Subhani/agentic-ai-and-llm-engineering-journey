# 10 — Production considerations and tradeoffs

## What this guide is about

Moving from **courseware** to **production** introduces reliability, cost, privacy, and monitoring concerns. This guide names the main tradeoffs touched by this module’s code patterns.

## Chunking and ingest cost

Advanced ingest calls an LLM **once per source file** and may use **`multiprocessing.Pool`**. If you hit rate limits:

```bash
export INSURELLM_INGEST_WORKERS=1
cd rag-system
python -m pro_implementation.ingest
```

**Example output:**

```text
Loaded 76 documents
100%|██████████| 76/76 [18:12<00:00, 14.37s/it]
Ingestion complete
```

What this output tells you: lowering parallelism **slows** wall-clock time but reduces burst traffic to the provider.

## Embeddings: API vs local

| Option | Latency | Cost | Privacy |
|--------|---------|------|---------|
| OpenAI API (`text-embedding-3-large`) | network hop | per-token | data leaves VPC |
| Local MiniLM / E5 | CPU/GPU bound | hardware | data stays on-box |

The baseline stack uses **OpenAI embeddings** for quality; `examples/02_embeddings_and_visualization.py` shows a **local** path.

## Vector database scaling

Chroma on disk is fine for demos. At higher QPS or multi-tenant isolation, teams often migrate to **managed vector search** or **Postgres + pgvector** for transactional consistency.

## Retrieval failure modes (examples)

| Symptom | Likely cause | Mitigation ideas |
|---------|----------------|------------------|
| Right answer, wrong citation | Model ignored context | Prompt tuning, citation forcing |
| Wrong numbers | Numeric chunk split badly | Smaller chunks around tables, tool-based lookup |
| “I don’t know” always | Retrieval k too low / wrong DB | Increase k, hybrid search |
| Slow answers | Huge context | Reduce `FINAL_K`, summarize chunks |

## Evaluation in production

Offline JSONL suites (like `tests.jsonl`) are **snapshots**. In production you also want:

- **Online metrics**: thumbs up/down, escalation rate,
- **Drift detection**: are questions shifting away from your test distribution?,
- **Periodic human audits** on stratified samples.

## Tenacity retries

Both advanced ingest and answer paths wrap fragile LLM calls with **`tenacity`** exponential backoff — in logs you might see repeated attempts during outages.

```text
Retrying __main__.process_document in 10 seconds ...
```

What this output tells you: the client is backing off instead of failing the whole ingest immediately.

## LiteLLM provider swaps

`pro_implementation` uses LiteLLM model ids like `openai/gpt-4.1-nano`. Switching providers is often **one environment variable**:

```bash
export INSURELLM_PRO_CHAT_MODEL="groq/llama-3.3-70b-versatile"
```

**Example output:**

```text
(depends on provider credentials; errors if key missing)
```

What this output tells you: unify routing under LiteLLM, but **each provider** still needs its own auth and error semantics.

## RAG vs fine-tuning (rule of thumb)

- Choose **RAG** when facts **change often** or must be **traceable** to documents.
- Choose **fine-tuning** when style/format is stable and proprietary, and data is static.

Most enterprise assistants combine **both** over time.

## What to remember

- Production is **ops + evaluation + architecture**, not only model choice.
- Treat this repo as a **learning sandbox** — harden security, PII handling, and access control before real customer data.

You finished Module 04 — return to [`README.md`](../README.md) for setup reminders anytime.
