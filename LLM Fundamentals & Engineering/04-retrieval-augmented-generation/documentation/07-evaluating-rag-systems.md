# 07 — Evaluating RAG systems

## What this guide is about

Why **retrieval** and **answers** must be measured separately, how this repo’s **`tests.jsonl`** is structured, and how [`evaluation/eval.py`](../rag-system/evaluation/eval.py) computes **MRR**, **nDCG**, and **keyword coverage**.

## Why evaluate RAG?

RAG can **look** successful while failing:

- retrieval returns **wrong** chunks (answer will be wrong or generic),
- retrieval is right but the model **ignores** the context,
- answers are right for the **wrong reasons** (memorization leakage).

You need automated checks to catch regressions when you change chunking, embeddings, or prompts.

## Ground truth file — `tests.jsonl`

Each JSON line becomes a `TestQuestion` in [`evaluation/test.py`](../rag-system/evaluation/test.py):

```python
from evaluation.test import load_tests

tests = load_tests()
print(tests[0].model_dump_json(indent=2))
```

**Example output:**

```json
{
  "question": "Who won the prestigious IIOTY award in 2023?",
  "keywords": ["Maxine", "Thompson", "IIOTY"],
  "reference_answer": "Maxine Thompson won the prestigious Insurellm Innovator of the Year (IIOTY) award in 2023.",
  "category": "direct_fact"
}
```

What this output tells you: **keywords** proxy “did we retrieve evidence containing these anchors?” while **reference_answer** supports judging generation quality (guide 08).

## Categories (examples)

| Category | Example question shape |
|----------|------------------------|
| `direct_fact` | Single document fact |
| `temporal` | Dates, timelines |
| `spanning` | Needs multiple docs |
| `comparative` | X vs Y |
| `numerical` | Counts, money |
| `relationship` | Who reports to whom |
| `holistic` | Broad summaries |

## Retrieval metrics — intuition

### Mean Reciprocal Rank (MRR)

For each keyword, find the **first** retrieved chunk containing that keyword (case-insensitive). Score = `1 / rank`. Average across keywords.

Worked micro-example (3 chunks, keyword `"IIOTY"`):

| Rank | Chunk contains keyword? |
|------|-------------------------|
| 1 | no |
| 2 | yes |

MRR = **0.5** because the first hit is at rank 2 → reciprocal = 1/2.

### nDCG@k (binary)

Chunks have relevance **1** if they contain the keyword else **0**. nDCG compares the **discount-weighted** gain of your ranking vs the **ideal** ordering (all relevant chunks pushed to the top).

### Keyword coverage

Percentage of keywords with **any** hit in the top-k set (MRR > 0).

## Run the small evaluation demo

```bash
cd rag-system
python examples/04_evaluation_demo.py
```

**Example output:**

```text
Loaded 150 tests from tests.jsonl

Sample test row #0:
  question: Who won the prestigious IIOTY award in 2023?
  keywords: ['Maxine', 'Thompson', 'IIOTY']
  category: direct_fact

Retrieval metrics:
  MRR: 0.8333
  nDCG: 0.9500
  keywords_found: 3/3
  keyword_coverage: 100.0%
```

What this output tells you: for this question the baseline retriever surfaced chunks containing **all** probe keywords — a strong retrieval pass (numbers vary with DB state).

## Full single-row CLI

```bash
cd rag-system
python evaluation/eval.py 0
```

**Example output (truncated):**

```text
================================================================================
Test #0
================================================================================
Question: Who won the prestigious IIOTY award in 2023?
...
Retrieval Evaluation
================================================================================
MRR: 0.8333
nDCG: 0.9500
Keywords Found: 3/3
Keyword Coverage: 100.0%

================================================================================
Answer Evaluation
================================================================================

Generated Answer:
 Maxine Thompson won the IIOTY award in 2023.

Feedback:
 The answer matches the reference ...
Scores:
  Accuracy: 5.00/5
  Completeness: 5.00/5
  Relevance: 5.00/5
```

What this output tells you: the harness first scores **retrieval**, then **generation + judge** (guide 08).

## Important limitation (read this twice)

`evaluation/eval.py` imports **`implementation.answer`**, not `pro_implementation`. If you change the advanced stack, **these numbers do not move** until you rewire imports.

## What to remember

- Evaluate **retrieval** and **answers** separately.
- Keywords are a **cheap proxy** for relevance — useful, not perfect.

Next: [`08-llm-as-a-judge.md`](08-llm-as-a-judge.md)
