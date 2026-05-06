# Original Notes for Module 03

This file keeps the rough source notes that inspired the module.

If you are learning the material, start with [README.md](README.md), then read [documentation/README.md](documentation/README.md). Those files are rewritten for beginners.

## Raw capture

Which is the best LLM?

That is not the best first question. A better question is:

> Which model is best for the task at hand?

Start with the basics:

- Parameters.
- Context window.
- Pricing.
- Open or closed model.
- Chat, reasoning, or hybrid behavior.
- Knowledge cutoff date.
- Training tokens.
- Inference cost.
- Training cost.
- Build cost.
- Time to market.
- Rate limit.
- Speed.

Then look at results:

- Benchmarks.
- Leaderboards.
- Arenas.

Chinchilla scaling law:

- A Google DeepMind idea about scaling models.
- Parameters should grow in balance with training tokens.
- If you get diminishing returns from more training data, this gives a useful rule of thumb.

Hard benchmarks:

- GPQA.
- MMLU-Pro.
- AIME.
- LiveCodeBench.
- MuSR.
- HLE.

Benchmark limits:

- Training-data contamination.
- The test may have leaked into training data.
- Some models may have seen the test or near-copies of it.

Leaderboards:

- Artificial Analysis.
- Vellum.
- Scale / SEAL.
- Hugging Face Open LLM Leaderboard.
- LiveBench.
- LM Arena / Chatbot Arena.

Commercial use cases:

- Automate.
- Augment.
- Differentiate.

Types of AI solutions:

- ChatGPT-style wrapper.
- Specialized AI platform on proprietary data.
- Agentic AI system.

Finding the business problem is part of the AI engineer role.

Example:

> I want to speak into my phone and ask, "What are my sales numbers today?"

Follow-up:

> What business problem does that solve?

AI engineers wear two hats:

- Data thinking.
- Software engineering.

Five-step strategy:

1. Understand the business problem.
2. Prepare by looking at problems and data.
3. Select a model.
4. Customize with RAG, tools, fine-tuning, or prompts when needed.
5. Productionize.

Practice project:

- Create a Python script that takes Python code and converts it to C++.
- Create a Python script that takes Python code and converts it to Rust.
- Create a system prompt and user prompt for this conversion task.
