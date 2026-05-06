# Documentation Guide

This folder contains the main reading path for module 03.

The module is about **model selection**. Model selection means choosing the LLM that best fits one job. The job could be "summarize support tickets," "answer questions from company documents," or "translate Python code to Rust."

## Important words before you start

- **LLM:** A large language model. It reads text and predicts useful next text.
- **Model:** The trained system that creates the answer.
- **Task:** The job you want the model to do.
- **Constraint:** A rule or limit, such as budget, speed, privacy, or output format.
- **Evaluation:** A test that helps you decide if the model is good enough.
- **Production:** The real version users depend on, not only a demo.

## Prerequisites

You can read this module by itself, but these earlier modules help:

- **Module 01:** [foundations.md](../../01-foundations/getting-started/foundations.md) explains tokens, context windows, transformers, APIs, and tool calling.
- **Module 02:** [documentation/README.md](../../02-open-source-models/documentation/README.md) explains open-weight models, Hugging Face, loading models, and tokenizers.

If a word is new, do not worry. This module gives short definitions before using important terms.

## Best reading order

1. [01-task-first-model-selection.md](01-task-first-model-selection.md)
2. [02-selection-criteria-costs-and-risk.md](02-selection-criteria-costs-and-risk.md)
3. [03-chinchilla-scaling-law.md](03-chinchilla-scaling-law.md)
4. [04-benchmarks-leaderboards-and-contamination.md](04-benchmarks-leaderboards-and-contamination.md)
5. [05-commercial-patterns-and-engineering-roles.md](05-commercial-patterns-and-engineering-roles.md)
6. [06-five-step-workflow-commercial-llm.md](06-five-step-workflow-commercial-llm.md)
7. [07-practice-code-translation-prompts-and-project.md](07-practice-code-translation-prompts-and-project.md)

## Hands-on practice

After guide 07, open [../code-translation/readme.md](../code-translation/readme.md).

That practice has a small Python script. A separate walkthrough explains the script line by line: [../code-translation/code-walkthrough.md](../code-translation/code-walkthrough.md).
