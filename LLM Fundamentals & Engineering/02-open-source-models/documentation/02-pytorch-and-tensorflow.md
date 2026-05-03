# PyTorch and TensorFlow

## What this guide is about

This guide explains what PyTorch and TensorFlow are, and why they matter even when you mostly use Hugging Face code.

You do not need advanced math for this page.
You only need a clear mental picture.

## Step 1: Why do we need frameworks?

Modern AI models use a lot of repeated math.
If every team wrote all of that math from zero, progress would be slow and many bugs would appear.

A framework is a library that gives us ready-made tools for this work.

These tools usually include:

- tensors for storing numbers
- model layers
- GPU support
- training utilities

So a framework is like a toolbox for model building and model running.

## Step 2: What is a tensor?

A tensor is a container of numbers.

It can be:

- a single list
- a table
- a bigger multi-step structure

Model inputs, outputs, and weights are usually stored as tensors.

If you are new, you can think of a tensor as:
"the main number format used inside deep learning code."

## Step 3: What is PyTorch?

PyTorch is an open-source Python framework used to build and run neural networks.

When you write:

```python
import torch
```

What this line means:

- `import` is the Python keyword used to load a library into your code.
- `torch` is the package name for PyTorch.
- After this line runs, you can use PyTorch tools such as `torch.Tensor`, `torch.nn`, and `torch.cuda`.

you get tools for:

- tensors
- GPU use
- model layers
- training and inference code

In many Hugging Face examples, PyTorch is the engine under the hood.

## Step 4: Why PyTorch matters in this module

Even if you do not build a model from zero, PyTorch still matters because:

- model weights are often stored in PyTorch format
- device names like `"cuda"` come from the PyTorch world
- quantization settings often use PyTorch data types such as `torch.bfloat16`
- Hugging Face model classes often wrap PyTorch modules

So when you load a model with Hugging Face, you are often still using PyTorch indirectly.

## Step 5: What is TensorFlow?

TensorFlow is another major deep learning framework.
It solves many of the same problems as PyTorch.

It can also:

- store tensors
- use GPUs
- train models
- run models

TensorFlow has been very important in research and industry.

## Step 6: Do I need both?

Not for this module.

It is useful to know that both exist, but most examples in this folder are closer to PyTorch.
So if you are a beginner, do not worry about learning both at the same time.

## Step 7: How this connects to Hugging Face

When you use Hugging Face with Python, a common flow is:

1. pick a model ID
2. load the tokenizer
3. load the model
4. run inference

Under the surface, Hugging Face often uses PyTorch to hold the tensors and run the math.

That is why people sometimes say:
"Hugging Face gives you the model interface, and PyTorch gives you the engine."

## What to remember

- A framework is a toolbox for model math.
- A tensor is the basic number container used by models.
- PyTorch and TensorFlow are both important frameworks.
- In this module, PyTorch is the one you will feel most often.
- Hugging Face usually sits on top of these lower-level tools.
