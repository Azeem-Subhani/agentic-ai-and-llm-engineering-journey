# Google Colab and GPUs

## What this guide is about

This guide explains what Google Colab is, why GPUs matter, and how to avoid the most common setup problems in this module.

If you are new to Colab, this page will save you time later.

## Step 1: What is Google Colab?

Google Colab is a website where you can run notebooks in the cloud.

A notebook is a file that mixes:

- written notes
- code cells
- outputs

This is useful because you can start learning and testing code without setting up everything on your own computer first.

## Step 2: What is a runtime?

A runtime is the temporary computer behind your notebook.

It can be:

- CPU only
- GPU enabled

The runtime is not permanent.
It can reset, disconnect, or change.
That is why code that worked an hour ago may stop working later if the runtime changes.

## Step 3: What is a GPU?

A GPU is a processor that is very good at large math tasks.
Many model examples run much faster on a GPU than on a CPU.

In this module, you may see a Tesla T4 in Colab.
That is a common cloud GPU for beginner model work.

You can check whether Colab gave you a GPU with:

```python
!nvidia-smi
```

What this line means:

- In a notebook, `!` means "run this as a shell command instead of normal Python code."
- `nvidia-smi` is an NVIDIA tool that shows GPU information.
- If a GPU is active, this command prints details such as the GPU name and memory.
- If no GPU is active, the output helps you see that too.

Example output from the course:

```text
Tesla T4
Success - Connected to a T4
```

## Step 4: What does "free GPU" really mean?

Free Colab can sometimes give you a GPU, but it does not promise one every time.

That means:

- one session may give you a GPU
- another session may give you only a CPU
- long sessions may be stopped

So it is best to think of free GPU access as a useful chance, not a fixed service.

## Step 5: How Colab helps learning

Colab is popular in courses because it gives you:

- quick startup
- shared notebooks
- cloud hardware
- less local setup

This is especially helpful when the course uses packages or GPU tools that are harder to install on a normal laptop.

## Step 6: How to connect Colab to Hugging Face

You do not connect the accounts in a special account-merging way.
Instead, you use a token.

The normal flow is:

1. create a Hugging Face token
2. add it in Colab secrets as `HF_TOKEN`
3. use `login(...)` in the notebook

This allows the notebook to download models that your account can access.

## Step 7: Paid GPUs

Some Colab plans offer stronger GPUs such as the A100.
These are useful for larger or faster runs.

But there is one important rule:
disconnect or stop the runtime when you finish.

If you leave a paid GPU running in the background, you may keep paying for time you are not using.

## Step 8: Hardware changes over time

GPU hardware changes fast.
A GPU that feels exciting today may feel normal next year.

This does not mean learning GPUs is a bad idea.
It only means buying hardware and renting hardware are different choices, and both have tradeoffs.

## Step 9: The most common confusing error

In Colab, a very common error looks like this:

```text
CUDA is required but not available for bitsandbytes
```

This often makes people think the package versions are broken.
But in many cases, the real problem is simpler:
Colab gave you a CPU runtime instead of a GPU runtime.

## Step 10: What to do when CUDA disappears

Try this in order:

1. disconnect and delete the runtime
2. reload the notebook
3. clear the outputs
4. reconnect to a GPU runtime
5. run the notebook again from the top

This is usually better than changing package versions immediately.

## What to remember

- Colab is a cloud notebook service.
- A runtime is the temporary machine behind the notebook.
- A GPU makes many model tasks much faster.
- Free GPU access is useful, but not guaranteed.
- If CUDA suddenly disappears, check the runtime before blaming the code.
