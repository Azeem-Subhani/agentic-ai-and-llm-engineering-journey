# Google Colab and GPUs

## What this guide is about

You will learn what **Google Colab** is, why your notebooks mention **Tesla T4** GPUs, how **free** tiers actually behave, and how to avoid surprise charges on **paid** GPUs. This guide also repeats the course’s **runtime troubleshooting** checklist verbatim—it is that important.

---

## Step 1 — What is Google Colab?

**Google Colab** (“Colaboratory”) is a **website** that runs **Jupyter notebooks** on Google’s computers instead of only on your laptop.

- A **notebook** mixes **markdown** explanations with **code cells** you run step by step.
- A **runtime** is the temporary virtual machine behind the notebook (CPU or GPU, with some preinstalled Python packages).

Colab is popular in courses because learners can start quickly without installing CUDA locally.

---

## Step 2 — What does “free GPU” really mean?

Your notes asked whether you can have a Colab with a **15 GB NVIDIA Tesla T4** “for free.”

**Accurate picture:**

- Free Colab **sometimes** offers **GPU** runtimes, commonly **T4** class on favorable days.
- Google **does not guarantee** a GPU every session, every hour, or every account. Busy periods, account limits, or policy changes can yield **CPU-only** runtimes.
- Even when you get a T4, **RAM and time limits** still apply; long jobs may be stopped.

So: treat a free T4 as a **helpful possibility**, not a contract.

---

## Step 3 — Collaboration

Colab notebooks can be stored in **Google Drive** or shared like other Google files. Multiple people can comment and run copies. That matches your note: it “allows you to collaborate.”

---

## Step 4 — Connecting Colab to your Hugging Face account

You do **not** “merge accounts” in a special way. The standard pattern is:

1. Create a Hugging Face **access token**.
2. Add it to Colab **Secrets** as `HF_TOKEN`.
3. Call `login(...)` in the first cells of the notebook (see any Week 3 notebook).

That lets `from_pretrained` download gated models you have been approved for.

---

## Step 5 — Paid GPUs (A100, etc.) and why “terminate” matters

Some Colab plans let you pick **premium GPUs** (for example **A100**) for faster or larger workloads.

**Rule:** When you finish, **disconnect or terminate** the runtime so you do not pay for idle GPU time you are not using. Your class notes called this out explicitly—treat it as a billing hygiene habit, not optional trivia.

---

## Step 6 — GPU obsolescence (from your notes)

Consumer and datacenter GPUs evolve quickly. A card that is “hot” today may be surpassed next year. Buying hardware can lock you into a depreciation curve; renting cloud GPUs shifts that tradeoff to hourly cost and availability.

This is context for career planning, not a reason to avoid learning GPUs—just a realistic note about **hardware churn**.

---

## Step 7 — The misleading `bitsandbytes` / CUDA error (copy this checklist)

Your notebooks warn that this error is **often not about broken package versions**:

> Runtime error: CUDA is required but not available for bitsandbytes…

**What usually happened:** Colab silently gave you a **CPU** runtime, or swapped your machine under load.

**Fix (follow in order):**

1. **Kernel menu → Disconnect and delete runtime**
2. Reload the notebook; **Edit → Clear all outputs**
3. Connect to a **new GPU** runtime (for example T4) using the top-right controls
4. **View resources** and confirm a GPU is visible
5. Rerun cells **from the top**, starting with `pip install` cells

If you skip step 1, you can chase version numbers for an hour and never fix the true cause.

---

## Step 8 — What you should remember

- Colab = **hosted notebooks** + **temporary runtimes**.  
- Free GPU access is **helpful but not guaranteed**.  
- Premium GPUs need **explicit shutdown discipline**.  
- The **bitsandbytes + CUDA** error is often a **runtime type** issue—use the checklist above.

You are ready for the hands-on guides: start with [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md).
