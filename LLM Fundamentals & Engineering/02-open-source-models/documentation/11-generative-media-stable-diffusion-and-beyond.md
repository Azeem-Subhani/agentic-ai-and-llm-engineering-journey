# Generative Media: Images and Audio

## What this guide is about

Most of this module focuses on text models.
This guide shows how the same open-model world also includes image and audio generation.

The aim is to give you a clean beginner map of the area.

## Step 1: What is generative media?

Generative media means models that create media instead of only classifying or summarizing it.

That media can include:

- images
- speech
- music
- video

So the big idea is simple:
the open-model ecosystem is not only about chat.

## Step 2: How image generation differs from text generation

A text model usually works by predicting the next token.

An image model often works differently.
Many image models use a diffusion process.

That means the model starts with noise and slowly turns that noise into an image.

So even though both are AI models, the internal process is not the same.

## Step 3: What is Stable Diffusion?

Stable Diffusion is a well-known family of open image models.

People use it for tasks such as:

- text-to-image
- image editing
- style changes

In this module, the example uses SDXL Turbo, which is a fast version of the SDXL family.

Turbo models are designed to create an image in very few steps.
That makes them good for quick experiments.

## Step 4: Simple SDXL Turbo example

Before the code, here are the important names:

- `AutoPipelineForText2Image` is a Hugging Face class that loads the right image-generation pipeline for a model.
- `from_pretrained(...)` is a common Hugging Face method that downloads saved model files and prepares them for use.
- `torch.float16` is a smaller number format that often saves GPU memory.

```python
from IPython.display import display
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe.to("cuda")

image = pipe(
    prompt="A class of students learning AI engineering in a vibrant pop-art style",
    num_inference_steps=4,
    guidance_scale=0.0,
).images[0]

display(image)
```

Line by line:

- `from IPython.display import display` imports the helper that shows the final image inside the notebook.
- `from diffusers import AutoPipelineForText2Image` imports the class used to load text-to-image pipelines.
- `import torch` imports PyTorch, which the pipeline uses under the hood.
- `pipe = AutoPipelineForText2Image.from_pretrained(...)` creates a pipeline object by loading saved model files.
- `"stabilityai/sdxl-turbo"` is the model ID on Hugging Face. It tells the code which model to download.
- `torch_dtype=torch.float16` asks the pipeline to use 16-bit floating point numbers, which often reduces memory use.
- `variant="fp16"` asks for the fp16 version of the model files when that version exists.
- `pipe.to("cuda")` moves the pipeline to the GPU. `"cuda"` is the common name used for NVIDIA GPU work in PyTorch code.
- `image = pipe(...)` runs the pipeline with your text prompt.
- `prompt="..."` is the text description of the image you want.
- `num_inference_steps=4` tells the model how many denoising steps to use. Fewer steps are faster, but may reduce detail.
- `guidance_scale=0.0` controls how strongly the model should follow the prompt. This setting is common in SDXL Turbo examples.
- `.images[0]` takes the first generated image from the returned result.
- `display(image)` shows the image inside the notebook.

The output is an image shown in the notebook.

## Step 5: What is a refiner?

Some image workflows use two stages:

1. a base model creates the first image
2. a refiner improves the details

This can help with things like:

- faces
- texture
- sharpness

The tradeoff is simple:
better detail often costs more time and memory.

## Step 6: Black Forest Labs and Flux

Black Forest Labs released the Flux family of image models.

From a beginner point of view, the important lesson is not only the brand name.
The important lesson is that new model families appear often, and each one may have:

- different loading code
- different hardware needs
- different licenses

So the safe habit is:
always read the model card before copying old code from a blog post.

## Step 7: Audio generation is not just one task

People often say "audio generation" as if it is one thing.
It is actually several different tasks.

For example:

- text-to-speech: text becomes spoken words
- text-to-audio: text becomes general sound
- text-to-music: text becomes music

These are related, but not the same.
A model built for speech is not always the right model for music.

## Step 8: The example in this module

The main audio-generation example in this module is text-to-speech.
It uses the model `microsoft/speecht5_tts`.

That example shows an important pattern:

1. load a model for a task
2. prepare the input
3. run the model
4. listen to or save the output

This same pattern appears again and again in open-model work.

## Step 9: Common beginner problems

When people try image or audio models for the first time, the most common problems are:

- not enough GPU memory
- missing packages
- missing Hugging Face login
- using the wrong task type

So if something breaks, first ask:

1. Do I have the right task?
2. Do I have the right model?
3. Do I have enough hardware?

## What to remember

- Open models are not only for text.
- Diffusion models are common for image generation.
- Stable Diffusion is an important image-model family.
- A refiner is a second step that improves an image.
- Audio generation includes different tasks such as speech and music.
- Always read the model card before using a new media model.
