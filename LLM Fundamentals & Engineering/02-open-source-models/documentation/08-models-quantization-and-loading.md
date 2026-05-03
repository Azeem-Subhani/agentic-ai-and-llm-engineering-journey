# Models, Quantization, and Loading

## How to use this guide

Follow [`../Week_3_Day_4_models.ipynb`](../Week_3_Day_4_models.ipynb) cell by cell while reading this document.

**Prerequisites:** [07-tokens-and-tokenizers.md](07-tokens-and-tokenizers.md) (chat templates, token IDs), [02-pytorch-and-tensorflow.md](02-pytorch-and-tensorflow.md) (what PyTorch is).

**Hardware:** Notebook expects a **CUDA GPU** (T4 is enough for smaller ids). Quantization reduces memory but does not remove the GPU requirement for these cells as written.

---

## Part A — Float precision without jargon first

### Why quantization exists

Model **weights** are numbers. If you store every weight as a **32-bit floating point** number (**float32**), you need **four bytes per weight**. A multi-billion-parameter model can exceed consumer GPU memory.

**Quantization** means storing or computing many weights with **fewer bits** so the model **fits** and sometimes runs faster, at some cost to numerical fidelity.

### The “dimmer switch” analogy (from class notes)

Think of a **dimmer switch** for lights:

- **Bright (more bits, e.g. float32):** finer control, more detail, more electricity (memory).  
- **Dim (fewer bits, e.g. 4-bit storage):** coarser steps, less detail, less electricity.

Training often uses wider numeric formats; **inference** can sometimes use dimmer formats and still look good.

### What this notebook uses

**4-bit NormalFloat (NF4)** quantization via **`bitsandbytes`** integrated with Hugging Face `BitsAndBytesConfig`. **bfloat16** is used for certain **compute** paths while weights are compressed—details are in the config walkthrough below.

---

## Part B — Cell-by-cell walkthrough

Notebook: `Week_3_Day_4_models.ipynb` — **30 cells** (indices **0–29**). Cell 29 is empty.

### Cell 0 — Markdown — Topic

Introduces the **lower-level** Transformers API: you work with **tokenizer + model** objects directly instead of only `pipeline`.

---

### Cell 1 — Markdown — Runtime pro-tip

Same misleading CUDA/bitsandbytes note—see [05](05-google-colab-and-gpus.md).

---

### Cell 2 — Code — Install dependencies

```python
!pip install -q --upgrade bitsandbytes accelerate transformers==4.57.6
```

- **`bitsandbytes`** — supplies 4-bit quantization kernels used when loading weights.
- **`accelerate`** — helps with device placement patterns (`device_map="auto"`).
- **`transformers`** — pinned version for reproducibility.

---

### Cell 3 — Code — Imports

```python
from google.colab import userdata
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
import torch
import gc
```

- **`AutoModelForCausalLM`** — “autoregressive” text model: predicts **next token** given previous tokens (GPT-style / Llama-style).
- **`TextStreamer`** — prints generated tokens to the console **as they arrive**.
- **`BitsAndBytesConfig`** — dataclass describing 4-bit load options for `from_pretrained`.
- **`gc` / `torch.cuda.empty_cache()`** — used later to free GPU memory between runs.

---

### Cell 4 — Markdown — HF login instructions

Same `HF_TOKEN` secret pattern as other days.

---

### Cell 5 — Code — Login

```python
hf_token = userdata.get('HF_TOKEN')
login(hf_token, add_to_git_credential=True)
```

Shorter than Day 3’s version—assumes you already know to set the secret.

---

### Cell 6 — Markdown — Llama access notes

Explains **gated** Meta Llama models on the Hub. You must accept terms on the model card.

---

### Cell 7 — Code — Model id strings

```python
# LLAMA = "meta-llama/Meta-Llama-3.1-8B-Instruct"
LLAMA = "meta-llama/Llama-3.2-1B-Instruct"

PHI = "microsoft/Phi-4-mini-instruct"
GEMMA = "google/gemma-3-270m-it"
QWEN = "Qwen/Qwen3-4B-Instruct-2507"
DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
```

**Line by line:**

- These are **strings** used later as Hub ids.  
- Comment/uncomment `LLAMA` to pick a larger or smaller Llama checkpoint.  
- **`Phi-4-mini-instruct`**, **`gemma-3-270m-it`**, etc., may each have their own license gates.

---

### Cell 8 — Code — Example chat messages

```python
messages = [
    {"role": "user", "content": "Tell a joke for a room of Data Scientists"}
  ]
```

OpenAI-style **role/content** list; will be converted by `apply_chat_template` (next section).

---

### Cell 9 — Markdown — More Llama licensing detail

Reinforces visiting the Meta model card; links troubleshooting Colab.

---

### Cell 10 — Code — Quantization configuration

```python
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)
```

**Field by field:**

- `load_in_4bit=True` — store (much of) the weights in **4-bit** form in GPU memory.
- `bnb_4bit_use_double_quant=True` — **double quantization**: quantize the **scaling constants** too, saving a bit more memory.
- `bnb_4bit_compute_dtype=torch.bfloat16` — some intermediate matmuls run in **brain float 16** (`bfloat16`), a 16-bit float format with the same exponent range as float32 (good stability vs classic float16).
- `bnb_4bit_quant_type="nf4"` — use the **NormalFloat4** data layout designed for neural net weights.

---

### Cell 11 — Markdown — 403 checklist

If `from_pretrained` fails with permission errors, verify login, token scopes, and model card access.

---

### Cell 12 — Code — Tokenize for Llama

```python
tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
```

**Line by line:**

- `from_pretrained(LLAMA)` — download tokenizer files for that checkpoint.
- `tokenizer.pad_token = tokenizer.eos_token` — many causal LMs lack a dedicated pad token; **reuse end-of-sequence token** as padding ID for batching safety.
- `apply_chat_template(..., return_tensors="pt")` — return a **PyTorch** tensor of token IDs shaped `[1, sequence_length]` (batch dimension 1).
- `.to("cuda")` — place input tensor on GPU RAM.

---

### Cell 13 — Code — Display `inputs`

Running `inputs` in a cell shows the tensor wrapper (dtype, device, shape). **Not human-readable text**—that is intentional pedagogy.

---

### Cell 14 — Code — Load quantized model

```python
model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto", quantization_config=quant_config)
```

**Line by line:**

- `AutoModelForCausalLM.from_pretrained` — instantiate the Python model class + load weights from Hub cache.
- `device_map="auto"` — let Accelerate heuristics spread layers across available GPUs (rare on Colab single GPU, but future-proof) and place weights intelligently.
- `quantization_config=quant_config` — apply the 4-bit recipe from cell 10.

**First run:** large download + slow load.

---

### Cell 15 — Code — Memory footprint

```python
memory = model.get_memory_footprint() / 1e6
print(f"Memory footprint: {memory:,.1f} MB")
```

**Interpretation:** Reports an approximate **GPU memory** usage for the loaded model object (implementation-defined but useful for comparisons before/after quantization).

---

### Cell 16 — Markdown — “Looking under the hood”

Explains that printing `model` shows **PyTorch modules** implementing the **Transformer** architecture; lists what to look for (embeddings, decoder layers, LM head). Points to optional deeper materials.

---

### Cell 17 — Code — Print the model object

```python
model
```

In Jupyter/Colab, showing `model` calls `repr` and prints a **tree** of submodule names (for example `LlamaDecoderLayer`, `LlamaSdpaAttention`, `LlamaMLP`, …).

**Next step after running:** read [09-inside-llama-decoder-architecture.md](09-inside-llama-decoder-architecture.md) for a line-by-line reading of a representative tree (sizes may differ by exact checkpoint; the guide explains what each block **means**).

---

### Cell 18 — Markdown — Source code rabbit hole

Links to the `transformers` GitHub repository for Llama implementations—optional reading.

---

### Cell 19 — Code — `generate` without streaming

```python
outputs = model.generate(inputs, max_new_tokens=80)
outputs[0]
```

**Line by line:**

- `generate` — autoregressive loop inside the library: repeatedly predicts next token until stop criteria.
- `max_new_tokens=80` — cap **new** tokens (excluding prompt length).
- `outputs[0]` — first (and only) batch row: 1D tensor of token IDs including the prompt.

---

### Cell 20 — Code — Decode to text

```python
tokenizer.decode(outputs[0])
```

Now you see the assistant continuation as a string (includes prompt + completion depending on tokenizer settings).

---

### Cell 21 — Code — Free GPU memory

```python
del model, inputs, tokenizer, outputs
gc.collect()
torch.cuda.empty_cache()
```

**Why:** Later cells load **other** models; CUDA OOM is common without cleanup.

---

### Cell 22 — Markdown — Streaming + generation prompts

Explains replacing plain `generate` with:

```python
streamer = TextStreamer(tokenizer)
outputs = model.generate(..., streamer=streamer)
```

and adding `add_generation_prompt=True` inside `apply_chat_template` so chat-tuned models know where to begin the assistant reply.

Link in notebook: [HF chat templating docs](https://huggingface.co/docs/transformers/main/en/chat_templating#what-are-generation-prompts).

---

### Cell 23 — Code — `generate` helper function

```python
def generate(model, messages, quant=True, max_new_tokens=80):
  tokenizer = AutoTokenizer.from_pretrained(model)
  tokenizer.pad_token = tokenizer.eos_token
  input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to("cuda")
  attention_mask = torch.ones_like(input_ids, dtype=torch.long, device="cuda")
  streamer = TextStreamer(tokenizer)
  if quant:
    model = AutoModelForCausalLM.from_pretrained(model, quantization_config=quant_config).to("cuda")
  else:
    model = AutoModelForCausalLM.from_pretrained(model).to("cuda")
  outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=max_new_tokens, streamer=streamer)
```

**Important naming note:** The **parameter** is called `model`, but callers pass a **string id** like `PHI` or `GEMMA`. Inside the function, that string is passed to `from_pretrained`. Reading call sites like `generate(PHI, messages)` makes this clear.

**Line by line:**

- Fresh `AutoTokenizer` per call—simple, not maximally efficient.
- `add_generation_prompt=True` — insert assistant-start markers for instruct checkpoints.
- `attention_mask = torch.ones_like(...)` — tells the model “all positions are real tokens; none are padding.” Still required when passing `input_ids` explicitly to `generate` in some configurations.
- `TextStreamer(tokenizer)` — live printing.
- `if quant:` branch — reload with **4-bit** config; else full precision **float weights** on GPU (only viable for small models like Gemma 270M on a T4).
- `model.generate(..., streamer=streamer)` — identical generation loop but prints incrementally.

**Return value:** The function does not `return` decoded text; **the streamer already printed** tokens to the cell output.

---

### Cell 24 — Code — Run Phi with quantization default

```python
generate(PHI, messages)
```

Uses `quant=True` default → 4-bit load.

---

### Cell 25 — Markdown — Gemma license gate

Google Gemma may require accepting terms on its Hub page.

---

### Cell 26 — Code — New joke prompt + Gemma full precision

```python
messages = [
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"}
  ]
generate(GEMMA, messages, quant=False)
```

**Why `quant=False`:** Tiny Gemma fits without 4-bit; also exercises the non-quantized branch.

---

### Cell 27 — Code — Qwen with default quant

```python
generate(QWEN, messages)
```

Larger than Gemma; 4-bit path is important on 16 GB GPUs.

---

### Cell 28 — Code — DeepSeek longer generation, no quant

```python
generate(DEEPSEEK, messages, quant=False, max_new_tokens=500)
```

**Tradeoff:** `quant=False` + larger token budget → **high VRAM** risk on Colab. If you OOM, switch to `quant=True` or shorter `max_new_tokens`.

---

### Cell 29 — Code — Empty

Ignore.

---

## Part C — Recap checklist

You should now be able to:

- Explain **4-bit NF4** at a high level and why `BitsAndBytesConfig` exists.
- Trace text → `apply_chat_template` → tensor on CUDA → `generate` → `decode`.
- Describe what `device_map="auto"` and `TextStreamer` accomplish.
- Read a printed `model` tree at a **high** level and know where to go for deeper layer meanings.

---

## Part D — Common errors

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CUDA OOM | Model too large for GPU / forgot cleanup | `del` + `empty_cache`; use smaller `LLAMA`; enable `quant=True` |
| 403 / gated | License not accepted | Model card → accept |
| `login` None | Missing `HF_TOKEN` secret | Add Colab secret |
| Slow every call | `generate()` reloads weights each invocation | For production, load once, reuse `model` object |

---

## Next guide

[09-inside-llama-decoder-architecture.md](09-inside-llama-decoder-architecture.md) explains the printed module tree line by line.
