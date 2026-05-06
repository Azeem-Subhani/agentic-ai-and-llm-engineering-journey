# Task-First Model Selection

## Goal

This guide teaches one habit:

> Start with the task before you choose the model.

An **LLM** is a large language model. A **model** is the trained system that gives an answer. A **task** is the job you want the model to do.

## Why "best LLM" is not enough

People often ask, "Which LLM is best?"

That question is incomplete. It does not say what the model must do.

A model can be very good at one task and weak at another task. For example:

- One model may write friendly emails well.
- Another model may solve hard math better.
- Another model may be cheaper and fast enough for support tickets.
- Another model may be safer for private company data.

The better question is:

> Which model is the best fit for this task, with these limits?

## What "fit" means

**Fit** means the model matches the real job.

Check these parts:

- **Input:** What text, code, files, or data will the model receive?
- **Output:** What should the model return?
- **Quality:** What counts as a good answer?
- **Speed:** How fast must the answer be?
- **Cost:** How much can each answer cost?
- **Privacy:** Can the data leave your company or device?
- **Risk:** What bad result must never happen?

These parts matter more than a model name.

## A simple task contract

A **task contract** is a short written description of the job. It makes the model choice easier.

Write it before testing models.

Example:

- **Task:** Turn a support ticket into a short summary.
- **Input:** One customer ticket, usually 200 to 1,000 words.
- **Output:** Three bullet points and one urgency label.
- **Success:** A support agent can understand the issue in under 30 seconds.
- **Failure:** The model must not invent a refund, a policy, or a promise.
- **Limits:** The answer should return in under 3 seconds and cost less than the team's budget.

Now the choice is clearer. You are not looking for a famous model. You are looking for a model that can pass this contract.

## How this changes model choice

Without a task contract, people compare models using vague words like "smart" or "best."

With a task contract, you can test useful things:

- Does the model follow the output format?
- Does it handle long inputs?
- Does it make dangerous mistakes?
- Is it fast enough?
- Is the cost acceptable?

## Beginner mistake to avoid

Do not start by choosing the largest model.

Start by finding the smallest, fastest, and cheapest model that meets the task contract. If it fails, move to a stronger model or improve the workflow.

## Recap

- "Best LLM" is not a complete question.
- Ask which model fits the task, limits, and risk.
- Write a short task contract before comparing models.

Next: [02-selection-criteria-costs-and-risk.md](02-selection-criteria-costs-and-risk.md).
