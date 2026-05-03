# What Are Open Source Models?

## What this guide is about

You will learn what people mean by **open source** in the world of large language models (LLMs), how that differs from closed services, and why a website called **Hugging Face** keeps appearing in courses like this one.

---

## Step 1 — What is a “model” here?

In everyday language, a **model** is a simplified description of something real. In machine learning, a **model** is a computer program plus a very large table of numbers (called **weights** or **parameters**) that were learned from data.

When you use an LLM, you are not “talking to a database of sentences.” You are running math that predicts likely next words (more precisely: **tokens**—see guide `07`) based on patterns learned from huge text collections.

---

## Step 2 — What does “open source” mean for LLMs?

There is no single legal definition everyone agrees on, but in practice people use the phrase in two related ways:

1. **Open weights**  
   The trained numbers (checkpoints) are published so you can download them and run the model yourself (subject to a **license** that may still forbid some commercial uses).

2. **Open code**  
   The **software** that loads and runs the model (for example training scripts or inference libraries) is published under an open-source license so you can read it, run it, and sometimes change it.

A model can be “open” in one sense but not the other. Always read the **model card** on the Hugging Face Hub (or the project’s README) for the exact rules.

---

## Step 3 — What is Hugging Face (in one calm paragraph)?

**Hugging Face** is a company and a website ([huggingface.co](https://huggingface.co)) that many people treat like “GitHub for ML artifacts.”

- **GitHub** is mainly for **source code** and version control.  
- **Hugging Face Hub** is mainly for sharing **models**, **datasets**, and small demo apps called **Spaces**.

Your class notes said “GitHub for the LLMs.” That is a good first mental picture: a place where communities upload models you can download, plus documentation (“model cards”) explaining what each model does and how to use it responsibly.

You do **not** need to understand Git deeply to use the Hub in a browser.

---

## Step 4 — Why would you use an open model instead of only ChatGPT-in-the-browser?

Reasons people mix both worlds:

- **Control and privacy:** You can run some models on your own computer or inside your company cloud, so sensitive text never leaves your environment.
- **Cost and batch work:** Running your own inference can be cheaper at large volume—or more expensive at small volume. There is no universal winner; it depends on scale and staffing.
- **Customization:** Open ecosystems make it easier to experiment with **fine-tuning** (later weeks) or connect models to your own tools.
- **Learning:** Reading open training or inference code helps you understand how systems are built.

Closed APIs (for example consumer chat products) can be excellent for fast iteration and strong baseline quality. Open models are another tool in the toolbox, not a moral requirement.

---

## Step 5 — What you should remember before the next guide

- An **LLM** is software plus **weights** that steer predictions.  
- **Open** usually means **you can access weights and/or code**, with a **license** that still matters.  
- **Hugging Face Hub** is the common place to **browse, download, and document** those models.

Next: [02-pytorch-and-tensorflow.md](02-pytorch-and-tensorflow.md) explains the programming frameworks that sit underneath most of these models.
