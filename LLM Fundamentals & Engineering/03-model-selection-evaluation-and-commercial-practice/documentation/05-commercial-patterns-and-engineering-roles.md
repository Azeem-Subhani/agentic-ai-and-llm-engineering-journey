# Commercial Patterns and Engineering Roles

## Goal

This guide explains how LLM projects show up in real businesses.

A **commercial project** is a project built for business use. It may serve customers, employees, or internal teams.

## Automate, augment, differentiate

A helpful product ladder is:

1. **Automate**
2. **Augment**
3. **Differentiate**

**Automate** means the AI does repeated work that humans do not need to do manually.

Examples:

- Tag support tickets.
- Draft a first reply.
- Extract names and dates from documents.

**Augment** means the AI helps a person do skilled work faster.

Examples:

- Suggest code changes to a developer.
- Help a lawyer search documents.
- Help a teacher draft practice questions.

**Differentiate** means the AI helps create something competitors cannot easily copy.

This often needs:

- Unique data.
- Deep workflow integration.
- Strong trust and safety.
- A better user experience.

Most teams should start with automate or augment. Jumping straight to differentiation can be expensive and unclear.

## Three common AI product types

These names are simple labels. Real products can mix them.

## 1. Wrapper around a general model

A **wrapper** is an app built around an existing model API. The app adds prompts, buttons, workflow, or a nicer interface.

Example:

- A company builds a chat assistant for its website using a model API.

Strength:

- Fast to build a demo.

Risk:

- Hard to defend if another team can copy it quickly.

## 2. Specialized platform on private data

A **specialized platform** uses company or domain data to solve a focused problem.

**Private data** means data that is not public, such as customer records, internal documents, or company workflows.

Common parts:

- RAG, which searches private documents and gives useful parts to the model.
- Permissions, so users only see data they are allowed to see.
- Audit logs, so the team can review what happened.
- Evaluation, so the team can measure quality.

Strength:

- More useful and harder to copy.

Risk:

- Takes more engineering, testing, and governance.

## 3. Agentic system

An **agentic system** is a system where the model can take steps and use tools.

A **tool** can be a calculator, database, code runner, search system, API, or file reader.

Example:

- A coding agent reads files, edits code, runs tests, and explains the change.

Strength:

- Can solve tasks that plain chat cannot.

Risk:

- Needs careful permissions, logging, tests, and rollback paths.

## Finding the real business problem

AI engineers do not only write prompts. They also help clarify the problem.

Example request:

> I want to speak into my phone and ask for today's sales numbers.

Before choosing a model, ask:

- Who needs the number?
- What decision changes because of the number?
- Which data source is correct?
- How fresh must the number be?
- What error would be dangerous?

The real problem may not be voice input. It may be slow reporting, unclear dashboards, or missing alerts.

## Two hats of an AI engineer

An AI engineer often wears two hats.

**Data hat:** You ask if the data is correct, useful, and testable.

**Software hat:** You build APIs, handle errors, protect secrets, write tests, and monitor the system.

Strong AI products need both.

## Recap

- Start with automate or augment before chasing differentiation.
- Know whether you are building a wrapper, a specialized platform, or an agentic system.
- Clarify the business problem before choosing a model.
- AI engineering needs data thinking and software engineering.

Next: [06-five-step-workflow-commercial-llm.md](06-five-step-workflow-commercial-llm.md).
