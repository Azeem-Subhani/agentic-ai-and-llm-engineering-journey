# 08 — LLM-as-a-judge

## What this guide is about

After RAG produces an answer, how do you **score** it automatically? This module uses **LLM-as-a-judge**: a second model call with a rubric returning structured scores.

## Why not string match?

Reference answers may be **paraphrased**. A correct answer might omit an adjective yet still be factually right. Regular expressions are brittle; a small judge model (here: `gpt-4.1-nano` via LiteLLM) reads **question + generated + reference** together.

## The `AnswerEval` schema

Defined in [`evaluation/eval.py`](../rag-system/evaluation/eval.py):

```python
from evaluation.eval import AnswerEval

sample = AnswerEval(
    feedback="Accurate and complete.",
    accuracy=5.0,
    completeness=4.0,
    relevance=5.0,
)
print(sample.model_dump_json(indent=2))
```

**Example output:**

```json
{
  "feedback": "Accurate and complete.",
  "accuracy": 5.0,
  "completeness": 4.0,
  "relevance": 5.0
}
```

What this output tells you: downstream dashboards consume **numeric** scores plus human-readable **feedback**.

## Judge prompt (shape)

The messages are:

1. **System**: “You are an expert evaluator…”
2. **User**: includes **Question**, **Generated Answer**, **Reference Answer**, asks for three 1–5 dimensions.

You can read the exact strings in `evaluate_answer()` inside `eval.py`.

## Calling the judge (minimal)

```bash
cd rag-system
python evaluation/eval.py 0
```

**Example output (excerpt):**

```text
Answer Evaluation
================================================================================

Generated Answer:
 Maxine Thompson won the IIOTY award in 2023.

Feedback:
 The generated answer matches the reference ...
Scores:
  Accuracy: 5.00/5
  Completeness: 5.00/5
  Relevance: 5.00/5
```

What this output tells you: the judge returned **structured** scores via LiteLLM `response_format=AnswerEval`.

## Tradeoffs

| Pros | Cons |
|------|------|
| Captures nuance better than keywords | Costs money + latency |
| Easy to iterate rubric text | Judge can be biased or inconsistent |
| Scales better than pure human review | Not a legal “source of truth” |

## Dashboard note

[`evaluator.py`](../rag-system/evaluator.py) batches all tests and renders HTML cards — see guide 09.

## What to remember

- **LLM-as-judge** is a **proxy metric** — tune prompts, spot-check failures, add human review for production.

Next: [`09-the-gradio-applications.md`](09-the-gradio-applications.md)
