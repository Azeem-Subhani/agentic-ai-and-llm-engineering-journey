# Open Source Models

This folder is a beginner-friendly guide to open models.
It is written in simple English and meant to be read in order.

The earlier version of this module had raw notes and notebooks.
That source material is now folded into these guides.
So the useful code, sample outputs, and key ideas are all here in the documentation.

## Who This Is For

This module is for readers who are new to:

- open models
- Hugging Face
- Colab
- tokenizers
- running models in Python

You do not need a strong machine learning background before you start.

## Best Reading Order

1. [01-what-are-open-source-models.md](01-what-are-open-source-models.md)
2. [02-pytorch-and-tensorflow.md](02-pytorch-and-tensorflow.md)
3. [03-hugging-face-ecosystem.md](03-hugging-face-ecosystem.md)
4. [04-ollama-vs-hugging-face-workflows.md](04-ollama-vs-hugging-face-workflows.md)
5. [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md)
6. [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md)
7. [07-tokens-and-tokenizers.md](07-tokens-and-tokenizers.md)
8. [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md)
9. [09-inside-llama-decoder-architecture.md](09-inside-llama-decoder-architecture.md)
10. [10-meeting-minutes-audio-product.md](10-meeting-minutes-audio-product.md)
11. [11-generative-media-stable-diffusion-and-beyond.md](11-generative-media-stable-diffusion-and-beyond.md)

## How The Guides Work

The first five guides explain the basic ideas.
They answer questions like:

- What is an open model?
- What is Hugging Face?
- What is the difference between Ollama and Hugging Face?
- Why does Colab matter?

The later guides show practical examples.
They answer questions like:

- How do I use a pipeline?
- What is a tokenizer?
- How do I load a model directly?
- How can I turn audio into meeting minutes?

This order matters because later guides use ideas from earlier ones.

## What You Need

For most examples, you need a free [Hugging Face](https://huggingface.co) account.
In Google Colab, add your token as a secret called `HF_TOKEN`.

For the optional OpenAI transcription path in guide `10`, add:

- `OPENAI_API_KEY`

For image generation, Whisper, and larger text models, a GPU is strongly recommended.

## Common Terms You Will Meet

| Term | Simple meaning |
|---|---|
| model | A trained program that learned patterns from data |
| weights | The learned numbers inside the model |
| inference | Using a trained model to get an output |
| token | A small piece of text the model reads as one unit |
| tokenizer | The tool that turns text into token IDs |
| pipeline | A ready-made Hugging Face function for a common task |
| quantization | Loading weights in a smaller format to save memory |
| gated model | A model that needs license approval before download |

If a word is new, the related guide explains it before using it in detail.

## Common Problems

| Problem | First thing to check |
|---|---|
| `403` when loading a model | Open the model page and accept the license |
| `401` or token error | Check `HF_TOKEN` in Colab secrets |
| CUDA is missing | Reconnect to a GPU runtime in Colab |
| Out of memory | Use a smaller model or use quantization |
| Audio file not found | Check your Google Drive path carefully |

## Goal Of This Module

By the end, you should be able to:

- explain what open models are
- understand the main Hugging Face tools
- use pipelines for text, image, and audio tasks
- understand what tokens and tokenizers do
- load a chat model with more control
- follow a simple end-to-end AI product example

The aim is not only to finish reading the pages.
The aim is to understand the ideas well enough that you can try the examples with confidence.
