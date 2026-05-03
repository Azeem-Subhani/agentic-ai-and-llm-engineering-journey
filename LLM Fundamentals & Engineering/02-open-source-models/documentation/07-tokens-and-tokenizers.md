# Tokens and Tokenizers

## How to use this guide

Walk alongside [`../Week_3_Day_3_tokenizers.ipynb`](../Week_3_Day_3_tokenizers.ipynb). This file explains **each cell in order** (markdown then code), defines **token**, **tokenizer**, **vocabulary**, **special tokens**, and shows how **chat templates** turn Python message lists into text the model was trained on.

**Prerequisites:** [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md) (Colab + `HF_TOKEN`), [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md) (inference vocabulary).

---

## Part A — Concepts in plain language

### What is a token?

A **token** is one symbol from a fixed list the model can read. Tokens are usually **subwords**: common words may be one token; rare words may split into several pieces.

### What is a tokenizer?

A **tokenizer** is code that:

1. **Encodes** text → list of integers (**token IDs**).
2. **Decodes** token IDs → text (not always identical to the original if whitespace was normalized).

### What is a vocabulary?

The **vocabulary** is the set of all tokens the tokenizer knows, each mapped to an integer ID.

### What is a special token?

A **special token** is a reserved symbol (with its own ID) that does not represent normal language text. Examples (exact strings depend on model family):

- Beginning / end of sequence markers  
- Padding markers when batching unequal lengths  
- Role markers for chat formats (`<|user|>`, `<|assistant|>`, etc. on some models)

They **signal structure** to the model: where the prompt starts, where the assistant answer should begin, etc.

---

## Part B — Cell-by-cell walkthrough

Notebook: `Week_3_Day_3_tokenizers.ipynb` — **26 cells** (indices **0–25**).

### Cell 0 — Markdown — Title

States the session goal: explore tokenizers; can run on CPU or locally.

---

### Cell 1 — Markdown — Colab pro-tips

Same bitsandbytes/CUDA runtime swap guidance as other notebooks—see [05](05-google-colab-and-gpus.md).

---

### Cell 2 — Code — Install pinned versions

```python
!pip install -q --upgrade datasets==3.6.0 transformers==4.57.6
```

Matches Day 2 pipelines notebook pinning for reproducibility.

---

### Cell 3 — Code — Imports

```python
from google.colab import userdata
from huggingface_hub import login
from transformers import AutoTokenizer
```

- **`AutoTokenizer`** — a factory class: given a model id string, it downloads the correct tokenizer class + vocabulary files (`tokenizer.json`, merges, etc.).

---

### Cell 4 — Markdown — Hugging Face sign-in instructions

Walks through token creation with **write** permissions and Colab secret `HF_TOKEN`.

---

### Cell 5 — Code — Login + optional GPU check

```python
hf_token = userdata.get('HF_TOKEN')
if hf_token and hf_token.startswith("hf_"):
  print("HF key looks good so far")
else:
  print("HF key is not set - please click the key in the left sidebar")
login(hf_token, add_to_git_credential=True)

gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
...
```

**Why `nvidia-smi` in a tokenizer lab?** Harmless sanity check; tokenizer cells themselves do not require GPU.

---

### Cell 6 — Markdown — Gated Llama access

Explains Meta’s **license acceptance** on the Hub for Llama weights. Follow the linked model card before `from_pretrained` calls.

---

### Cell 7 — Code — Load Llama 3.1 base tokenizer

```python
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3.1-8B', trust_remote_code=True)
```

**Line by line:**

- `'meta-llama/Meta-Llama-3.1-8B'` — Hub id for the **base** (non-Instruct) Llama 3.1 8B tokenizer files (tokenizer often shared across related checkpoints).
- `trust_remote_code=True` — allows execution of custom code shipped with some tokenizers/models on the Hub when needed.

**403 errors:** Accept license; confirm token; see troubleshooting links in the notebook markdown.

---

### Cell 8 — Code — `encode`

```python
text = "I am excited to show Tokenizers in action to my LLM engineers"
tokens = tokenizer.encode(text)
tokens
```

**Line by line:**

- `encode(text)` — returns a Python **list of ints** (token IDs), typically including **special** start/end tokens depending on tokenizer defaults.
- The last line `tokens` in a notebook displays the list.

**Expected pattern:** More tokens than words, because subword splitting.

---

### Cell 9 — Code — Count characters, words, tokens

```python
character_count = len(text)
word_count = len(text.split(' '))
token_count = len(tokens)
print(f"There are {character_count} characters, {word_count} words and {token_count} tokens")
```

**Teaching point:** **Tokens are not words.** Pricing and context windows are measured in tokens.

---

### Cell 10 — Code — `decode` full sequence

```python
tokenizer.decode(tokens)
```

**Round-trip:** Usually returns text equivalent to the original aside from spacing normalization.

---

### Cell 11 — Code — `batch_decode` on a flat list

```python
tokenizer.batch_decode(tokens)
```

**Caution:** `batch_decode` expects a **list of lists** (one sequence per row). Passing a flat list of ints can behave unexpectedly depending on version; the notebook uses it as a teaching moment—observe the output shape.

**Mental model:** Prefer `decode(tokens)` for a single sequence; use `batch_decode([[1,2,3],[4,5]])` for batches.

---

### Cell 12 — Code — Added vocabulary

```python
# tokenizer.vocab
tokenizer.get_added_vocab()
```

- `get_added_vocab()` — mapping of **extra** tokens (often special tokens) added beyond the base merge table.

---

### Cell 13 — Code — Vocabulary size

```python
len(tokenizer.vocab)
```

- Reports how many token entries the tokenizer’s vocabulary object exposes (exact internals differ between “slow” and “fast” tokenizers, but the number is useful intuition).

---

### Cell 14 — Markdown — Instruct models

**Key idea:** **Instruct** checkpoints are fine-tuned for **chat-style** prompts. They expect a structured string (system/user/assistant), not raw freeform only.

---

### Cell 15 — Code — Load Instruct tokenizer

```python
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3.1-8B-Instruct', trust_remote_code=True)
```

Note different Hub string than cell 7—**Instruct** tokenizer includes chat template metadata.

---

### Cell 16 — Code — `apply_chat_template` (string output)

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"}
  ]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
print(prompt)
```

**Line by line:**

- `messages` — Python objects convenient for **application code** (like OpenAI’s API shape).
- `apply_chat_template(...)` — converts those roles into **one string** using the model’s training-time conventions.
- `tokenize=False` — return **text**, not token IDs.
- `add_generation_prompt=True` — append markers that cue the model to **begin assistant generation** (exact string depends on model family).

**Why this matters:** The neural net still only sees **token IDs** after you encode this prompt string.

---

### Cell 17 — Markdown — “Aha” moment

States the core fact: LLMs consume **sequences of integers**; messages are converted → tagged text → tokens → IDs. Probability over **next token ID**.

Read this section slowly—it bridges application APIs and math.

---

### Cell 18 — Markdown — Upcoming models

Introduces Phi 4, DeepSeek 3.1, Qwen Coder examples below.

---

### Cell 19 — Code — Model id constants

```python
PHI4 = "microsoft/Phi-4-mini-instruct"
DEEPSEEK = "deepseek-ai/DeepSeek-V3.1"
QWEN_CODER = "Qwen/Qwen2.5-Coder-7B-Instruct"
```

These are **Hub ids**; some may be large or gated—downloads can take time and disk.

---

### Cell 20 — Code — Compare encode + batch_decode across Llama vs Phi

```python
phi4_tokenizer = AutoTokenizer.from_pretrained(PHI4)

text = "I am curiously excited to show Hugging Face Tokenizers in action to my LLM engineers"
print("Llama:")
tokens = tokenizer.encode(text)
print(tokens)
print(tokenizer.batch_decode(tokens))
print("\nPhi 4:")
tokens = phi4_tokenizer.encode(text)
print(tokens)
print(phi4_tokenizer.batch_decode(tokens))
```

**Teaching point:** Same English string becomes **different integer sequences** because vocabularies and pre-tokenizers differ.

---

### Cell 21 — Code — Compare chat templates (Llama vs Phi)

```python
print("Llama:")
print(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print("\nPhi 4:")
print(phi4_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

**Teaching point:** Same logical `messages` list becomes **different prompt strings**—each model family’s recipe.

---

### Cell 22 — Code — Add DeepSeek tokenizer + numeric comparison

```python
deepseek_tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK)

text = "I am curiously excited to show Hugging Face Tokenizers in action to my LLM engineers"
print(tokenizer.encode(text))
print()
print(phi4_tokenizer.encode(text))
print()
print(deepseek_tokenizer.encode(text))
```

Shows three ID sequences side by side.

---

### Cell 23 — Code — Chat templates for three models

Prints `apply_chat_template` strings for Llama, Phi, DeepSeek with the same `messages`.

---

### Cell 24 — Code — Qwen Coder tokenization of Python code

```python
qwen_tokenizer = AutoTokenizer.from_pretrained(QWEN_CODER)
code = """
def hello_world(person):
  print("Hello", person)
"""
tokens = qwen_tokenizer.encode(code)
for token in tokens:
  print(f"{token}={qwen_tokenizer.decode(token)}")
```

**Line by line:**

- The loop prints each **integer id** and a **decode** attempt for that id alone.
- **Note:** `decode([token_id])` is the usual robust pattern for per-id pieces; if `decode(token)` misbehaves on some versions, mentally substitute decoding a one-element list.

**Teaching point:** Code tokenizers often split on meaningful programmer substrings (indentation, operators).

---

### Cell 25 — Markdown — Empty / end

No additional content in export—end of notebook.

---

## Part C — Recap checklist

You should now be able to:

- Define **token**, **tokenizer**, **vocabulary**, **special token** without hand-waving.
- Predict that **word count ≠ token count** for English text.
- Explain why `apply_chat_template` exists and what `add_generation_prompt=True` is for.
- Read a printed list of token IDs as “the real input” to the LM.

---

## Part D — Common errors

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 403 on Llama | License not accepted | Visit model card, accept terms |
| `HF_TOKEN` invalid | Secret off or typo | Toggle Colab secret access |
| Huge downloads | Large tokenizer bundles | Wait, or pick smaller demo model ids for practice |

---

## Next guide

[08-models-quantization-and-loading.md](08-models-quantization-and-loading.md) loads full **causal LMs** with optional **4-bit quantization**.
