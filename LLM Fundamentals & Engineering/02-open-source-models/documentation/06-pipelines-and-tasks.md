# Pipelines and Common NLP Tasks

## How to use this guide

Open the notebook [`../week_3_day_2_pipelines.ipynb`](../week_3_day_2_pipelines.ipynb) in **Google Colab** (upload or open from Drive) or in **Jupyter** on your machine. This document walks **every cell in order**: markdown first (ideas), then code (line by line).

**Prerequisites:** Read [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md) for GPU runtime setup and the `HF_TOKEN` secret.

---

## Part A — Concepts before code

### What is a Hugging Face `pipeline`?

A **`pipeline`** is a **high-level Python function** returned by `transformers.pipeline(...)`. It bundles:

1. Choosing (or defaulting) a **model** for a named **task** (for example “sentiment-analysis”).
2. Loading a **tokenizer** when needed.
3. Moving tensors to a **device** like `"cuda"`.
4. Applying sensible **pre- and post-processing** so you pass plain strings and get plain Python objects back.

Your notes called this the “higher level API” compared to manually combining `AutoTokenizer` + `AutoModel*` (we do that in Day 4—see [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md)).

### What is inference?

**Inference** means using a model **after** it was trained, to produce outputs on new inputs. The notebook contrasts this with **training** (updating weights). All `pipeline` examples here are inference-only.

---

## Part B — Cell-by-cell walkthrough

Notebook: `week_3_day_2_pipelines.ipynb` — **23 cells**, indices **0–22**. (Cell 22 is an empty code cell in the export you have.)

### Cell 0 — Markdown — Welcome

**Goal:** Introduce the two-level API idea and the syntax pattern:

1. `my_pipeline = pipeline("task_name")`
2. `result = my_pipeline(input)`

**Vocabulary:**

- **Task:** a string name like `"sentiment-analysis"` that tells Hugging Face which kind of model to load.

---

### Cell 1 — Markdown — Colab pro-tips

**Goal:** Set expectations about warnings and the misleading **bitsandbytes / CUDA** error.

**Takeaway:** If that error appears mid-notebook, treat it as a **runtime lost GPU** problem first. Full checklist: [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md#step-7--the-misleading-bitsandbytes--cuda-error-copy-this-checklist).

---

### Cell 2 — Markdown — Training vs inference

**Goal:** Define **training** (update weights; includes **fine-tuning** if starting from a pretrained model) vs **inference** (fixed weights).

**Why it matters:** Pipelines are for inference. The notebook says later weeks will train models with lower-level APIs.

---

### Cell 3 — Code — Pin library versions

```python
!pip install -q --upgrade datasets==3.6.0 transformers==4.57.6
```

**Line by line:**

- `!` — shell escape in Jupyter/Colab: run a terminal command from the notebook.
- `pip install` — Python package installer.
- `-q` — quieter logs.
- `--upgrade` — if an older version is installed, replace it.
- `datasets==3.6.0` — exact version of the `datasets` library (reproducibility).
- `transformers==4.57.6` — exact version of `transformers` used when the course was recorded.

**Why at the top:** If the runtime restarts, you must rerun installs before imports.

**Note:** Image generation later uses `diffusers`. If a later cell fails with `ModuleNotFoundError: diffusers`, add a cell `!pip install -q diffusers` (version pinning optional). Colab sometimes preinstalls it; environments differ.

---

### Cell 4 — Code — Check GPU (`nvidia-smi`)

```python
gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Not connected to a GPU')
else:
  print(gpu_info)
  if gpu_info.find('Tesla T4') >= 0:
    print("Success - Connected to a T4")
  else:
    print("NOT CONNECTED TO A T4")
```

**Line by line:**

- `gpu_info = !nvidia-smi` — Colab “magic”: run the `nvidia-smi` system command and capture its text lines into `gpu_info` (a special list-like object depending on IPython version; joining is defensive).
- `'\n'.join(gpu_info)` — one multiline string for easy substring search.
- `find('failed')` — crude detection if the command did not run as expected.
- `find('Tesla T4')` — course checks specifically for **T4**; other GPUs (L4, A100) still work for many cells but your printout may say “NOT CONNECTED TO A T4” even though CUDA is fine.

**Expected output:** A table showing GPU name, memory, driver version, plus the success line if a T4 is present.

---

### Cell 5 — Code — Imports

```python
import torch
from google.colab import userdata
from huggingface_hub import login
from transformers import pipeline
from diffusers import DiffusionPipeline
from datasets import load_dataset
import soundfile as sf
from IPython.display import Audio
```

**Line by line:**

- `torch` — PyTorch; used later for dtypes/devices in diffusion and audio cells.
- `userdata` — **Colab-only**: reads **Secrets** like `HF_TOKEN`. In local Jupyter, this import fails—use environment variables instead.
- `login` — authenticates your session to the Hugging Face Hub.
- `pipeline` — the high-level Transformers API for NLP/audio tasks.
- `DiffusionPipeline` — imported here; the image cell actually uses `AutoPipelineForText2Image` (imported inside that cell). `DiffusionPipeline` is a generic entrypoint in `diffusers`; harmless if unused, or historical import.
- `load_dataset` — loads the speaker embedding dataset in the TTS section.
- `soundfile` — reads/writes audio arrays to disk if needed (import present for ecosystem compatibility; the shown TTS path may not write files directly).
- `Audio` — IPython helper to **play** audio in the notebook output.

---

### Cell 6 — Markdown — Hugging Face account

**Goal:** Ensure every learner has a Hub account, a **write-capable** token, and Colab secret access toggled on.

---

### Cell 7 — Code — Log in to the Hub

```python
hf_token = userdata.get('HF_TOKEN')
if hf_token and hf_token.startswith("hf_"):
  print("HF key looks good so far")
else:
  print("HF key is not set - please click the key in the left sidebar")
login(hf_token, add_to_git_credential=True)
```

**Line by line:**

- `userdata.get('HF_TOKEN')` — fetch secret by name; `None` if missing.
- `startswith("hf_")` — Hugging Face user tokens conventionally start with `hf_` (not a cryptographic guarantee, just a quick sanity check).
- `login(hf_token, add_to_git_credential=True)` — stores credentials for this session so model downloads work; `add_to_git_credential` also tries to configure git credential helper (mainly relevant if you clone from Hub with git).

**Failure modes:** Forgot to toggle secret visibility; token without write scope; expired token.

---

### Cell 8 — Markdown — How `pipeline` works

**Key API:**

```python
my_pipeline = pipeline(task, model=xx, device=xx)
```

- **`task`:** string like `"ner"`.
- **`model=`** optional: Hub model id; if omitted, a default model is chosen.
- **`device=`** `"cuda"` for NVIDIA GPU, `"mps"` for Apple Silicon GPU, `"cpu"` otherwise.

Then call `my_pipeline(input)` repeatedly.

---

### Cell 9 — Code — Sentiment analysis (default model)

```python
my_simple_sentiment_analyzer = pipeline("sentiment-analysis", device="cuda")
result = my_simple_sentiment_analyzer("I'm super excited to be on the way to LLM mastery!")
print(result)
```

**Line by line:**

- `pipeline("sentiment-analysis", device="cuda")` — build a callable object; first run may **download weights**.
- The string argument is the **review text**.
- `print(result)` — typically a **list of dicts** like `[{'label': 'POSITIVE', 'score': 0.99...}]` (exact numbers vary by model).

**Interpretation:** `label` is the predicted class; `score` is a confidence-like probability for that class under the model’s softmax.

---

### Cell 10 — Code — Second sentiment string

Same pipeline object, new string—shows the API is reusable.

**Expected shape:** Still a list of one dict; label may flip toward negative phrasing.

---

### Cell 11 — Code — Sentiment with an explicit multilingual model

```python
better_sentiment = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", device="cuda")
result = better_sentiment("I should be more excited to be on the way to LLM mastery!!")
print(result)
```

**Line by line:**

- `model="nlptown/bert-base-multilingual-uncased-sentiment"` — full Hub id `author/model`.
- This model outputs **star-like labels** (1–5) in many course runs; your exact label strings appear in `print(result)`.

**Why specify a model?** Defaults change over time; a pinned id makes tutorials reproducible.

---

### Cell 12 — Code — Named Entity Recognition (NER)

```python
ner = pipeline("ner", device="cuda")
result = ner("AI Engineers are learning about the amazing pipelines from HuggingFace in Google Colab from Ed Donner")
for entity in result:
  print(entity)
```

**Line by line:**

- `"ner"` — task tag for token-classification style entity spans.
- `result` — list of dicts with keys such as `entity`, `score`, `word`, `start`, `end` (exact schema can vary slightly by model version).
- The `for` loop prints **one entity per line**.

**How to read an entity dict:** `entity` often looks like `B-PER` (begin person) or `B-ORG` (begin organization) in IOB tagging schemes.

---

### Cell 13 — Code — Extractive Question Answering

```python
question="What are Hugging Face pipelines?"
context="Pipelines are a high level API for inference of LLMs with common tasks"

question_answerer = pipeline("question-answering", device="cuda")
result = question_answerer(question=question, context=context)
print(result)
```

**Line by line:**

- **Extractive QA** means the answer must be a **span copied from the context**, not free-written.
- `question_answerer(question=..., context=...)` — keyword arguments are required; order is easy to confuse.
- `result` — typically includes `score`, `start`, `end`, and `answer` text.

---

### Cell 14 — Code — Summarization

```python
summarizer = pipeline("summarization", device="cuda")
text = """ ... long paragraph ... """
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print(summary[0]['summary_text'])
```

**Key arguments:**

- `max_length` / `min_length` — soft bounds on output length in **tokens** (tokenizer-dependent), not strict word counts.
- `do_sample=False` — greedy or beam-like deterministic decoding (depends on inner defaults); avoids randomness for demos.

**Output shape:** `summary` is a list; element `0` has key `'summary_text'`.

---

### Cell 15 — Code — English → French translation (default model)

```python
translator = pipeline("translation_en_to_fr", device="cuda")
result = translator("The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API.")
print(result[0]['translation_text'])
```

**Shape:** `result` is a list of dicts; French text lives under `translation_text`.

---

### Cell 16 — Code — English → Spanish with explicit model

```python
translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es", device="cuda")
result = translator("The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API.")
print(result[0]['translation_text'])
```

**Why show Helsinki-NLP?** Demonstrates how to pick a specific **Marian / OPUS** style model from the Hub’s translation collection.

---

### Cell 17 — Code — Zero-shot classification

```python
classifier = pipeline("zero-shot-classification", device="cuda")
result = classifier("Hugging Face's Transformers library is amazing!", candidate_labels=["technology", "sports", "politics"])
print(result)
```

**Concept:** The model scores how well the text matches **each candidate label** without task-specific fine-tuning on your labels.

**Typical output keys:** `labels` (ranked list), `scores` (parallel list of probabilities).

---

### Cell 18 — Code — Text generation

```python
generator = pipeline("text-generation", device="cuda")
result = generator("If there's one thing I want you to remember about using HuggingFace pipelines, it's")
print(result[0]['generated_text'])
```

**Behavior:** Continues the prompt. The returned string usually **includes the original prompt** plus new tokens; that is why the key is `generated_text` for many GPT-style pipelines.

---

### Cell 19 — Code — Text-to-image (SDXL Turbo)

```python
from IPython.display import display
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")
prompt = "A class of students learning AI engineering in a vibrant pop-art style"
image = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0.0).images[0]
display(image)
```

**Line by line:**

- `AutoPipelineForText2Image` — factory that picks a concrete pipeline class for SDXL.
- `from_pretrained("stabilityai/sdxl-turbo", ...)` — download/load weights for that Hub id.
- `torch_dtype=torch.float16` — compute many activations in **16-bit floating point** to save memory; requires GPU support.
- `variant="fp16"` — some models ship multiple weight formats; this picks the fp16 checkpoint files when present.
- `pipe.to("cuda")` — move the pipeline’s PyTorch modules to GPU.
- `num_inference_steps=4` — SDXL Turbo is designed for **very few** denoising steps (fast, lower fidelity than slow samplers).
- `guidance_scale=0.0` — for this turbo recipe, classifier-free guidance is effectively disabled (model-specific behavior).
- `.images[0]` — PIL image object.
- `display(image)` — renders inline in Colab.

**VRAM warning:** SDXL class models can be tight on **16 GB** GPUs; if you OOM, try a smaller image model or CPU offloading (advanced; not in this cell).

---

### Cell 20 — Code — Text-to-speech (SpeechT5)

```python
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch
from IPython.display import Audio

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device='cuda')
embeddings_dataset = load_dataset("matthijs/cmu-arctic-xvectors", split="validation", trust_remote_code=True)
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
speech = synthesiser("Hi to an artificial intelligence engineer, on the way to mastery!", forward_params={"speaker_embeddings": speaker_embedding})

Audio(speech["audio"], rate=speech["sampling_rate"])
```

**Line by line:**

- `pipeline("text-to-speech", "microsoft/speecht5_tts", ...)` — loads SpeechT5 TTS weights.
- `load_dataset(..., trust_remote_code=True)` — some datasets execute a loading script from the Hub; this flag acknowledges that behavior.
- `embeddings_dataset[7306]` — picks one **fixed** speaker embedding row for reproducibility.
- `torch.tensor(...).unsqueeze(0)` — shape `(1, dim)` batch dimension expected by the model.
- `forward_params={"speaker_embeddings": ...}` — passes extra tensors into the model forward pass (voice timbre control).
- `speech["audio"]` — waveform array; `sampling_rate` tells the player how many samples per second.

**Expected output:** playable audio widget in Colab.

---

### Cell 21 — Markdown — Where to find the full pipeline task lists

**Transformers pipelines:** [Hugging Face docs — Pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines)

**Diffusers pipelines overview:** [Diffusers API overview](https://huggingface.co/docs/diffusers/en/api/pipelines/overview)

---

### Cell 22 — Code — Empty

No code—placeholder or accidental empty cell. Safe to ignore.

---

## Part C — Recap checklist

After running the notebook top to bottom on a healthy GPU runtime, you should be able to:

- Explain **inference** vs **training**.
- Create a `pipeline` for at least three distinct **task strings**.
- Interpret **NER** dicts, **QA** span answers, and **zero-shot** label lists.
- Describe at a high level what **SDXL Turbo** and **SpeechT5 TTS** cells are doing (even if you do not memorize every argument).

---

## Part D — Common errors

| Symptom | Likely cause | First fix |
|---------|--------------|-----------|
| `CUDA ... bitsandbytes` | CPU runtime or runtime swap | [05](05-google-colab-and-gpus.md) checklist |
| `401/403` on download | Missing/invalid token or gated model | Fix `HF_TOKEN`; accept model license |
| `ModuleNotFoundError: diffusers` | Package not installed | `pip install diffusers` |
| OOM on SDXL | Not enough GPU memory | Smaller model / fewer concurrent pipelines |

---

## Next guide

[07-tokens-and-tokenizers.md](07-tokens-and-tokenizers.md) explains how text becomes token IDs—the missing piece before Day 4’s `generate`.
