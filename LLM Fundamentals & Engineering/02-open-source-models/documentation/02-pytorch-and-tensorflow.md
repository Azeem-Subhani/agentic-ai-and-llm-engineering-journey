# PyTorch and TensorFlow

## What this guide is about

You will learn what a **deep learning framework** is, why courses keep mentioning **PyTorch** and **TensorFlow**, and how that connects to the line you will see in the Day 4 notebook: a Hugging Face **model object** is “a neural network implemented in PyTorch.”

No calculus is required here—only clear pictures.

---

## Step 1 — What problem do frameworks solve?

A modern language model is built from many repeated building blocks (layers of math). If programmers had to write every low-level operation by hand for every project, progress would be slow and buggy.

A **deep learning framework** is a library that provides:

- **Tensors:** multi-dimensional arrays (think tables of numbers) that can live in **CPU** or **GPU** memory.
- **Automatic differentiation:** a way to compute how small changes in weights affect an error signal—used heavily during **training**.
- **GPU acceleration:** operations batched so a graphics card can run them efficiently.
- **Building blocks:** common layer types (linear layers, attention, activation functions) already implemented and tested.

**PyTorch** and **TensorFlow** are two popular frameworks. Both are widely used in research and industry. Hugging Face **Transformers** is implemented primarily in **PyTorch** today for most model definitions you will touch in class.

---

## Step 2 — What is PyTorch, in plain language?

**PyTorch** is an open-source Python library from Meta (with a large community) for building and running neural networks.

When you run:

```python
import torch
```

you gain access to `torch.Tensor` objects and layers like `torch.nn.Linear`. A full model is often a Python **class** whose `forward` method describes how data flows from input to output.

In the course notebooks, you rarely write raw PyTorch layer-by-layer for Llama—**Hugging Face** already did that—but you still benefit from PyTorch because:

- The **weights** are stored in PyTorch tensors.
- **Device** placement (`"cuda"` vs `"cpu"`) is PyTorch vocabulary.
- **Quantization** helpers (see guide `08`) integrate with PyTorch dtypes such as `torch.bfloat16`.

---

## Step 3 — What is TensorFlow?

**TensorFlow** is an open-source framework from Google (with a large ecosystem). It is another way to define tensors, run them on GPU, and train models.

Some models or tools in the wild are released with TensorFlow checkpoints, but the **Hugging Face Transformers** code path used in your Week 3 notebooks is **PyTorch-first**. If you see TensorFlow mentioned in older blog posts, treat it as an alternative ecosystem, not a requirement for these exercises.

---

## Step 4 — How this connects to “running a model yourself”

When your notes contrast **Ollama** vs **Hugging Face** (see guide `04`), the Hugging Face path often means:

- You choose a **model id** on the Hub.
- Python libraries download **configuration** and **weights**.
- A **PyTorch module** inside Transformers holds those weights and runs **inference**.

So “running it yourself” does **not** mean you hand-type matrix multiplications. It means **your Python process** loads public weights and executes the open implementation, instead of sending every prompt to someone else’s HTTP API.

---

## Step 5 — What you should remember

- A **framework** supplies tensors, GPU support, and neural building blocks.  
- **PyTorch** is the framework directly under most HF `AutoModel*` classes you will use.  
- **TensorFlow** is a major alternative ecosystem; you do not need it for the Week 3 notebooks listed in [README.md](README.md).

Next: [03-hugging-face-ecosystem.md](03-hugging-face-ecosystem.md) maps the main Hugging Face **libraries** to jobs they do.
