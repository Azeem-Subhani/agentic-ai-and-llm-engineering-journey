# What Are Open Source Models?

## What this guide is about

This guide explains three basic ideas:

1. what a model is
2. what "open source" means in this area
3. why Hugging Face appears so often in open-model work

The goal is to build the right mental picture before we look at code.

## Step 1: What is a model?

In machine learning, a model is a program that learned patterns from data.

When you give the model a new input, it uses those patterns to produce an output.
For a language model, the output is usually the next piece of text.

It is easy to imagine a model as a box full of saved sentences.
That is not how it works.
A language model does not search a big list of ready-made answers.
It runs math on learned patterns and predicts what should come next.

## Step 2: What are weights?

The learned numbers inside a model are called weights.
Some people also call them parameters.

You can think of weights as the part of the model that stores what it learned during training.
When people say "download the model weights," they mean downloading those learned numbers.

## Step 3: What does "open source" mean here?

In the world of LLMs, people often use "open source" in a loose way.
Usually they mean one or both of these things:

1. Open weights  
   You can download the trained model and run it yourself.

2. Open code  
   You can read and use the software that loads or trains the model.

This is why two models can both be called "open" even if they are not open in exactly the same way.

## Step 4: Open does not mean "no rules"

Even when a model is open, it may still have a license.
A license explains what you are allowed to do with the model.

For example, a license may place rules on:

- commercial use
- redistribution
- safety requirements

So the safe beginner habit is:
always open the model page and read the license notes before using the model in a real project.

## Step 5: What is Hugging Face?

Hugging Face is a company, a website, and a set of tools.

The website is where many people share:

- models
- datasets
- demos
- documentation

A simple first mental picture is:

- GitHub is mainly for source code
- Hugging Face is mainly for machine learning models and datasets

This picture is not perfect, but it is useful when you are starting.

## Step 6: Why do people use open models?

People use open models for different reasons.

### More control

You can choose the model, the hardware, and the way you run it.
That gives you more freedom than using only a closed web product.

### Privacy

Some teams want to run models inside their own machine or cloud account.
That can be helpful when the text is private.

### Cost

At some scales, running your own model can be cheaper.
At other scales, a hosted API can be cheaper.
There is no single winner for every case.

### Learning

Open tools make it easier to see how real systems are built.
This is one reason open models are great for study.

## Step 7: Open models and closed APIs can both be useful

This is important:
open models are not the only good option.

Closed APIs are often easier to start with.
They can also give very strong results.

Many real teams use both:

- closed APIs for speed and convenience
- open models for control, learning, or special use cases

## What to remember

- A model is a trained program, not a big list of saved answers.
- Weights are the learned numbers inside the model.
- "Open" can mean open weights, open code, or both.
- A license still matters.
- Hugging Face is the main place you will use in this module.
