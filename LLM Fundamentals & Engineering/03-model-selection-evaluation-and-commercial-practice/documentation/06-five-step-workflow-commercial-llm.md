# Five-Step Workflow for Commercial LLM Projects

## Goal

This guide gives you a repeatable path from idea to production.

**Production** means real users depend on the system. A production system needs tests, monitoring, security, and a way to recover from failure.

## Step 1: Understand the business problem

Start with the business problem, not the model.

Write a short problem statement:

- Who is the user?
- What are they trying to do?
- What decision or action depends on the answer?
- What does success look like?
- What must never happen?

Example:

- "Support agents need a short summary of long tickets so they can respond faster without missing important customer details."

Checkpoint:

- You can explain the project to a non-technical person in two sentences.

## Step 2: Prepare the data and evaluation

**Data** is the text, code, documents, logs, or records the system uses.

**Evaluation** is how you test whether the system is good enough.

Prepare before choosing a model.

Do this:

- List the top 3 to 5 real tasks.
- Find the correct data sources.
- Create 20 to 50 small test examples.
- Write a simple scoring rule.
- Decide which failures are serious.

Checkpoint:

- You can test two models on the same examples and compare the results.

## Step 3: Select a model

Use the task contract and checklist from the earlier guides.

Compare:

- Quality on your examples.
- Context window.
- Cost.
- Speed.
- Privacy rules.
- Freshness needs.
- Risk level.

Choose a primary model and a fallback model when possible.

**Fallback model** means another model or workflow you can use if the first one fails, becomes too expensive, or is unavailable.

Checkpoint:

- You can explain why this model fits this task better than the alternatives.

## Step 4: Customize only when needed

**Customize** means changing the workflow so the model performs better for your task.

Common customization options:

- **Prompting:** Give clearer instructions.
- **RAG:** Search your documents first, then send the useful parts to the model.
- **Tool calling:** Let the model ask your code to run a tool, such as a database query.
- **Fine-tuning:** Train a model further on examples.

Do not customize because it sounds advanced. Customize because a test shows the current approach is not good enough.

Checkpoint:

- Each customization improves a measured result.

## Step 5: Productionize

**Productionize** means making the feature safe and reliable enough for real use.

Include:

- Logging that does not expose secrets.
- Error handling and retries.
- Rate limit handling.
- Model and prompt version tracking.
- Human review for high-risk outputs.
- Cost monitoring.
- Tests before model or prompt changes.
- A rollback plan.

**Rollback** means returning to a previous safe version if the new version fails.

Checkpoint:

- The team knows what to do if quality drops, cost spikes, or a provider has an outage.

## Common failure mode

Teams often spend too much time choosing models before they understand the problem or build an evaluation set.

This creates a flashy demo but a weak product.

## Recap

- Understand the problem first.
- Prepare data and evaluation before model shopping.
- Select a model using task, cost, speed, and risk.
- Customize only when tests show it helps.
- Production is engineering, not just prompting.

Next: [07-practice-code-translation-prompts-and-project.md](07-practice-code-translation-prompts-and-project.md).
