# Benchmarks, Leaderboards, and Contamination

## Goal

This guide explains how to read model scores without trusting them too much.

A **benchmark** is a fixed test. It has questions, tasks, and scoring rules.

A **leaderboard** is a public ranking table. It shows model scores from one or more benchmarks.

## Why benchmarks exist

Benchmarks help people compare models in a repeatable way.

For example, a coding benchmark may give each model the same programming problems. The score may count how many solutions pass tests.

This is useful because every model receives the same challenge.

But a benchmark is not your real product. A high score does not guarantee success on your private data, your users, or your risk rules.

## Common benchmark names

Benchmark names can change over time. New versions may replace old versions. Always read the official benchmark description when the score matters.

Here are simple meanings for names you may hear:

| Name | Simple meaning |
| --- | --- |
| GPQA | Hard graduate-level science questions. |
| MMLU-Pro | A broad test across many school and professional topics. |
| AIME | Competition-style math problems. |
| LiveCodeBench | Coding problems where answers can be tested by running code. |
| MuSR | Multi-step reasoning tasks. |
| HLE | Very hard expert-level questions across many subjects. |

These scores are signals. They are not final proof.

## Training-data contamination

**Training-data contamination** means test data may have appeared in the model's training data.

This matters because the model might remember the answer instead of solving the problem.

Example:

- A benchmark question is posted online.
- A training dataset collects that page.
- A model trains on the page.
- Later, the model is tested on the same or very similar question.

The score may look better than the model's real ability.

## Other benchmark limits

Benchmarks can miss real product problems.

Common limits:

- They often measure average performance, not rare but serious failures.
- They may not test long company documents.
- They may not test tool use.
- They may not test your exact output format.
- They become stale when models improve or test data leaks.

Use benchmarks to make a shortlist. Then test on your own examples.

## Leaderboards and arenas

An **arena** is a system where humans compare two model answers, often without knowing which model wrote each answer.

Common places people discuss:

- **Artificial Analysis:** Compares model quality, price, speed, and context size.
- **Vellum:** Often compares API cost, context size, and model choices.
- **SEAL leaderboards:** Enterprise-focused model rankings.
- **Hugging Face Open LLM Leaderboard:** Focuses on open-weight models.
- **LiveBench:** Tries to reduce contamination by using fresher tasks.
- **LMSYS Chatbot Arena:** Uses human votes to compare chat answers.

These tools are useful for discovery. They are not a replacement for your own evaluation.

## A safe way to use scores

Use this order:

1. Write your task contract.
2. Use benchmarks to find candidate models.
3. Test those models on 20 to 50 real examples.
4. Compare quality, cost, speed, and risk.
5. Keep testing after launch.

## Recap

- Benchmarks are fixed tests with scores.
- Leaderboards rank models, but they can become stale.
- Contamination can inflate scores.
- Your task-specific evaluation matters most.

Next: [05-commercial-patterns-and-engineering-roles.md](05-commercial-patterns-and-engineering-roles.md).
