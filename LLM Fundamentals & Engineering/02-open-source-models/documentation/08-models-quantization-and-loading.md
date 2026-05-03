# Models, Quantization, and Loading

## What this guide is about

In guide `06`, you used pipelines.
Pipelines are easy because they hide many details.

In this guide, you go one level lower.
You work directly with:

- a tokenizer
- a model
- generation settings

This guide explains that code in simple English.

## Step 1: Why use the lower-level API?

Sometimes you want more control than a pipeline gives you.

For example, you may want to control:

- which model is loaded
- how the prompt is built
- how generation runs
- how memory is saved

That is why people often move from `pipeline(...)` to model objects like `AutoModelForCausalLM`.

## Step 2: What is a causal language model?

A causal language model is a model that predicts the next token from the tokens that came before it.

This is the common setup for chat-style text generation.

When you ask such a model a question, it answers by generating one token, then the next, then the next.

## Step 3: Why quantization exists

Large models need a lot of memory.
If the weights are stored in a large number format, some models will not fit on your GPU.

Quantization means storing weights in a smaller format so the model can fit more easily.

Simple picture:

- more bits = more memory
- fewer bits = less memory

The tradeoff is that smaller formats may lose some detail, but often the model still works well enough for inference.

## Step 4: Basic setup

Before the code, here are the important names:

- `AutoTokenizer` loads the correct tokenizer for a model ID
- `AutoModelForCausalLM` loads a text-generation model
- `TextStreamer` prints tokens as the model generates them
- `BitsAndBytesConfig` stores quantization settings

```python
!pip install -q --upgrade bitsandbytes accelerate transformers==4.57.6

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextStreamer,
    BitsAndBytesConfig,
)
import torch
import gc
```

Line by line:

- `!pip install ...` installs the packages used in this guide.
- `bitsandbytes` is the library that helps with 4-bit model loading.
- `accelerate` helps with device placement and larger model workflows.
- `transformers==4.57.6` installs the specific `transformers` version used here.
- `from transformers import (...)` imports the Hugging Face classes used in the guide.
- `import torch` imports PyTorch.
- `import gc` imports Python's garbage-collection helper, which is useful when cleaning memory later.

## Step 5: Pick model IDs

A model ID is the name used on Hugging Face to identify one exact model.

```python
LLAMA = "meta-llama/Llama-3.2-1B-Instruct"
PHI = "microsoft/Phi-4-mini-instruct"
GEMMA = "google/gemma-3-270m-it"
QWEN = "Qwen/Qwen3-4B-Instruct-2507"
DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
```

Line by line:

- `LLAMA = "meta-llama/Llama-3.2-1B-Instruct"` stores the model ID for one Llama instruct model.
- `PHI = "microsoft/Phi-4-mini-instruct"` stores the model ID for one Phi model.
- `GEMMA = "google/gemma-3-270m-it"` stores the model ID for one Gemma model.
- `QWEN = "Qwen/Qwen3-4B-Instruct-2507"` stores the model ID for one Qwen model.
- `DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"` stores the model ID for one DeepSeek model.

Some of these models need license approval on Hugging Face first.

## Step 6: Build a 4-bit config

`BitsAndBytesConfig` is a class that stores quantization settings.
It does not load the model by itself.
It only stores the options you want to use later.

```python
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
)
```

Line by line:

- `quant_config = BitsAndBytesConfig(...)` creates one quantization settings object and stores it in `quant_config`.
- `load_in_4bit=True` tells the model loader to use 4-bit weights.
- `bnb_4bit_use_double_quant=True` asks for extra memory saving through double quantization.
- `bnb_4bit_compute_dtype=torch.bfloat16` says that some model calculations should use the `bfloat16` number format.
- `torch.bfloat16` is a 16-bit floating-point format used often in modern model work.
- `bnb_4bit_quant_type="nf4"` selects the 4-bit weight format called NF4, which is made for neural-network weights.

## Step 7: Turn chat messages into model input

Before the code, here are the important names:

- `AutoTokenizer` is the Hugging Face helper that loads the correct tokenizer for a model ID
- `from_pretrained(...)` downloads saved tokenizer files and prepares them
- `apply_chat_template(...)` turns a message list into the prompt format the model expects

```python
messages = [
    {"role": "user", "content": "Tell a joke for a room of Data Scientists"}
]

tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
print(inputs)
```

Line by line:

- `messages = [...]` creates a list with one chat message.
- `"role": "user"` says this message is from the user.
- `"content": "..."` holds the actual text of the message.
- `tokenizer = AutoTokenizer.from_pretrained(LLAMA)` loads the tokenizer that matches the model ID stored in `LLAMA`.
- `from_pretrained(...)` is the method that downloads saved files if needed and then loads them.
- `tokenizer.pad_token = tokenizer.eos_token` sets the padding token to be the same as the end-of-sequence token.
- `pad_token` is used when inputs need padding.
- `eos_token` means end-of-sequence token.
- `inputs = tokenizer.apply_chat_template(...)` formats the message list and turns it into model-ready input.
- `messages` is the chat data being formatted.
- `return_tensors="pt"` asks the tokenizer to return a PyTorch tensor instead of plain text.
- `"pt"` means PyTorch.
- `.to("cuda")` moves the resulting tensor to the GPU.
- `print(inputs)` prints the tensor.

Output idea:

```text
A PyTorch tensor of token IDs on the GPU
```

## Step 8: Load the model

Before the code, here are the important names:

- `AutoModelForCausalLM` is a Hugging Face class for text-generation models
- `device_map="auto"` lets the library choose device placement

```python
model = AutoModelForCausalLM.from_pretrained(
    LLAMA,
    device_map="auto",
    quantization_config=quant_config,
)
```

Line by line:

- `model = AutoModelForCausalLM.from_pretrained(...)` loads the text-generation model and stores it in `model`.
- `LLAMA` is the model ID to load.
- `device_map="auto"` lets the library choose how to place the model on the available device or devices.
- `quantization_config=quant_config` tells the loader to use the 4-bit settings created earlier.

This is the main loading step.
It may take time the first time because files need to download.

## Step 9: Check memory use

```python
memory = model.get_memory_footprint() / 1e6
print(f"Memory footprint: {memory:,.1f} MB")
```

Line by line:

- `model.get_memory_footprint()` asks the model for an estimate of how much memory it uses.
- `/ 1e6` changes the value into roughly megabytes.
- `print(f"...")` prints a formatted string.
- `:,.1f` is Python formatting that keeps one decimal place and adds commas when needed.

Expected result:

```text
Memory footprint: ... MB
```

The exact number depends on the model.

## Step 10: Generate text

`generate(...)` is the main method used to ask the model for a reply.

```python
outputs = model.generate(inputs, max_new_tokens=80)
print(tokenizer.decode(outputs[0]))
```

Line by line:

- `outputs = model.generate(inputs, max_new_tokens=80)` asks the model to continue the input.
- `inputs` is the tensor created earlier from the chat messages.
- `max_new_tokens=80` tells the model to generate up to 80 new tokens.
- `print(tokenizer.decode(outputs[0]))` turns the first output row back into text and prints it.
- `outputs[0]` means "take the first generated sequence."
- `decode(...)` turns token IDs into readable text.

Output idea:

```text
The original prompt followed by the model's reply
```

## Step 11: Stream the answer live

`TextStreamer` is a helper class that prints tokens as they appear.

```python
streamer = TextStreamer(tokenizer)
outputs = model.generate(inputs, max_new_tokens=80, streamer=streamer)
```

Line by line:

- `streamer = TextStreamer(tokenizer)` creates a streamer object that knows how to decode the generated token IDs.
- `tokenizer` is passed in so the streamer can turn token IDs into text.
- `outputs = model.generate(...)` runs generation again.
- `streamer=streamer` tells the model to send new tokens to the streamer as they appear.

This prints tokens as they are produced.
It feels more like a chat app.

## Step 12: A reusable helper

This helper wraps the same steps into one function.

```python
def generate(model_id, messages, quant=True, max_new_tokens=80):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True,
    ).to("cuda")
    attention_mask = torch.ones_like(input_ids, dtype=torch.long, device="cuda")
    streamer = TextStreamer(tokenizer)
    if quant:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quant_config,
        ).to("cuda")
    else:
        model = AutoModelForCausalLM.from_pretrained(model_id).to("cuda")
    model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        streamer=streamer,
    )
```

Before reading the lines, here are the function parameters:

- `model_id` is the Hugging Face model ID to load
- `messages` is the chat message list
- `quant=True` means use quantization by default
- `max_new_tokens=80` means generate up to 80 new tokens by default

Line by line:

- `def generate(...):` defines a reusable Python function called `generate`.
- `tokenizer = AutoTokenizer.from_pretrained(model_id)` loads the tokenizer for the given model ID.
- `tokenizer.pad_token = tokenizer.eos_token` sets the padding token.
- `input_ids = tokenizer.apply_chat_template(...)` formats the message list and returns PyTorch token IDs.
- `return_tensors="pt"` asks for PyTorch tensors.
- `add_generation_prompt=True` adds the assistant-start marker so the model knows it should answer.
- `.to("cuda")` moves the token IDs to the GPU.
- `attention_mask = torch.ones_like(input_ids, dtype=torch.long, device="cuda")` creates a mask tensor with the same shape as `input_ids`.
- `torch.ones_like(...)` means "make a new tensor of ones with the same shape."
- `dtype=torch.long` sets the integer type used for the mask.
- `device="cuda"` puts the mask on the GPU.
- `streamer = TextStreamer(tokenizer)` creates the streamer object.
- `if quant:` checks whether quantization should be used.
- `model = AutoModelForCausalLM.from_pretrained(..., quantization_config=quant_config).to("cuda")` loads the model with 4-bit settings and moves it to the GPU.
- `else:` is the non-quantized path.
- `model = AutoModelForCausalLM.from_pretrained(model_id).to("cuda")` loads the model without 4-bit settings and moves it to the GPU.
- `model.generate(...)` runs the actual generation.
- `input_ids=input_ids` passes in the tokenized prompt.
- `attention_mask=attention_mask` passes in the mask.
- `max_new_tokens=max_new_tokens` uses the chosen output length limit.
- `streamer=streamer` streams the output as it appears.

This helper was used in the old notebook to try several models with the same prompt.

## Step 13: Try different models

```python
generate(PHI, messages)
generate(GEMMA, messages, quant=False)
generate(QWEN, messages)
generate(DEEPSEEK, messages, quant=False, max_new_tokens=500)
```

Line by line:

- `generate(PHI, messages)` runs the helper with the Phi model and the default settings.
- `generate(GEMMA, messages, quant=False)` runs the Gemma model without quantization.
- `quant=False` means "load the model without the 4-bit config."
- `generate(QWEN, messages)` runs the Qwen model with the default quantized path.
- `generate(DEEPSEEK, messages, quant=False, max_new_tokens=500)` runs DeepSeek without quantization and allows a much longer answer.
- `max_new_tokens=500` tells the model it can generate more tokens than the default.

Simple rule:

- larger models often need quantization
- smaller models can sometimes run without it

## Step 14: Clean up memory

```python
del model, inputs, tokenizer, outputs
gc.collect()
torch.cuda.empty_cache()
```

Line by line:

- `del model, inputs, tokenizer, outputs` removes those variables from the current Python scope.
- `gc.collect()` asks Python to clean up unused objects.
- `torch.cuda.empty_cache()` asks PyTorch to release cached GPU memory that is no longer needed.

This helps when you want to load another model in the same runtime.

## What to remember

- `AutoTokenizer` loads the correct tokenizer for a model.
- `AutoModelForCausalLM` loads a text-generation model.
- `from_pretrained(...)` loads saved model or tokenizer files.
- `BitsAndBytesConfig` stores quantization settings.
- `generate(...)` is the method that asks the model to continue the prompt.
- Understanding the parameters helps you control model loading instead of only copying code.
