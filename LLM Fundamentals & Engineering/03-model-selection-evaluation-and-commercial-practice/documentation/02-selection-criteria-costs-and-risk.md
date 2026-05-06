# Selection Criteria: Cost, Speed, and Risk

## Goal

This guide gives you a simple checklist for comparing LLMs.

A **criterion** is one thing you use to judge a choice. For example, cost is a criterion. Speed is another criterion.

## 1. Parameters

**Parameters** are learned numbers inside a model. They are also called **weights**.

You may see names like 7B, 8B, or 70B. The letter **B** means billion. A 7B model has about 7 billion parameters.

Why this matters:

- More parameters can help a model learn more patterns.
- More parameters often cost more to run.
- More parameters can make the model slower.

Important: bigger is not always better. A smaller model can be better for a narrow task if it is cheaper, faster, or trained for that task.

## 2. Context Window

A **token** is a small piece of text. It can be a word, part of a word, punctuation, or space-like text.

A **context window** is the maximum number of tokens the model can read at one time.

Why this matters:

- If your document is too long, the model may not see all of it.
- If the model cannot see the needed text, it may answer badly.
- Long context usually costs more.

If your input is too long, common fixes are:

- **Chunking:** Split the text into smaller parts.
- **Summarizing:** Compress the text before sending it.
- **Retrieval:** Search for only the most useful parts and send those.
- **RAG:** Retrieval-augmented generation. This means the app searches your data first, then gives the model the found text.

## 3. Open and Closed Models

A **closed API model** is a model you call through a company service. You send input to the service and receive output back.

An **open-weight model** is a model where the model weights are available to download, based on its license.

Why this matters:

- Closed API models are often easy to start using.
- Open-weight models can be hosted by you or your company.
- Licenses, privacy rules, cost, and maintenance are different for each path.

Do not assume "open" means "free for any use." Always read the license.

## 4. Behavior Type

**Behavior type** means the kind of work the model is designed to do well.

Common types:

- **Chat model:** Good at conversation and instruction following.
- **Reasoning model:** Good at harder, multi-step thinking, often with more time or cost.
- **Hybrid model:** Offers both fast chat and deeper reasoning modes.

Choose the behavior type from the task contract. For example, a live chat support bot may need speed. A legal review assistant may need slower but more careful reasoning.

## 5. Knowledge Freshness

A **knowledge cutoff** is the date after which the model may not know new facts from training.

Why this matters:

- A model may not know today's prices, laws, bugs, or company data.
- A newer model name does not solve every freshness problem.

If freshness matters, connect the model to tools, search, databases, or RAG.

## 6. Cost

Cost is more than the price on a model page.

Check these cost layers:

- **Inference cost:** The cost to run the model for each request.
- **Input tokens:** Tokens you send to the model.
- **Output tokens:** Tokens the model writes back.
- **Fine-tuning cost:** The cost to train a model on extra examples.
- **Build cost:** Engineering time to build and test the feature.
- **Support cost:** Monitoring, fixing bugs, and handling failures.

The cheapest model per token may not be the cheapest full system if it needs many retries or human fixes.

## 7. Speed and Rate Limits

**Latency** means how long the user waits for an answer.

A **rate limit** is a maximum number of requests or tokens allowed in a period of time.

Why this matters:

- A slow model can hurt the user experience.
- A rate limit can block your app during busy hours.
- A faster model may be better even if it is a little less accurate.

## 8. Risk

Risk means the cost of a bad answer.

Common risks:

- **Hallucination:** The model says something false as if it is true.
- **Data leakage:** Private data is exposed to the wrong place.
- **Compliance issue:** The system breaks a law, policy, or industry rule.
- **Vendor outage:** A provider is down and your feature stops working.
- **Model change:** A provider updates or removes a model your app depends on.

High-risk tasks need stronger checks, human review, logging, and safe fallback plans.

## A simple checklist

Before choosing a model, answer these questions:

- What is the task?
- How long are the real inputs?
- How fast must the answer be?
- What is the budget?
- Is private data involved?
- Does the answer need fresh facts?
- What happens if the model is wrong?
- How will we test quality?

## Recap

Good model selection checks parameters, context, openness, behavior type, freshness, cost, speed, and risk.

Next: [03-chinchilla-scaling-law.md](03-chinchilla-scaling-law.md).
