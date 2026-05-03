# Meeting Minutes from Audio (End-to-End Product)

## How to use this guide

Walk through [`../Week_3_Day_5_Meeting_Minutes_product.ipynb`](../Week_3_Day_5_Meeting_Minutes_product.ipynb) with this page open.

**Prerequisites:** [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md) (pipelines, ASR task), [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md) (Llama + 4-bit + `generate`).

**Secrets:** You need **`HF_TOKEN`** for Hugging Face paths. For **Option 2** transcription you also need **`OPENAI_API_KEY`** in Colab secrets.

---

## Part A — What this notebook builds

**Goal:** Turn a **recording of speech** into **written meeting minutes** (summary, discussion, takeaways, action items).

**Stages:**

1. **STEP 1 — Transcribe audio** to plain text (two alternative implementations).  
2. **STEP 2 — Analyze** the transcript with an **instruction-tuned Llama** model to emit structured markdown minutes.

This is a realistic pattern for “AI product” assignments: **specialized model for audio** + **general LLM for writing**.

---

## Part B — Cell-by-cell walkthrough

Notebook: `Week_3_Day_5_Meeting_Minutes_product.ipynb` — **23 cells** (indices **0–22**). Cell 22 is empty.

### Cell 0 — Markdown — Dataset context

Explains the **Denver City Council** audio clip, gives a Google Drive download link, and points to the **MeetingBank** Hugging Face dataset for the curious.

**Your job before code runs:** obtain an `.mp3` file (provided extract or your own).

---

### Cell 1 — Markdown — Colab runtime pro-tip

Same CUDA/bitsandbytes false alarm guidance—[05](05-google-colab-and-gpus.md).

---

### Cell 2 — Code — Install packages

```python
!pip install -q --upgrade bitsandbytes accelerate transformers==4.57.6
```

**Note:** The next cell imports `openai`. If that import fails on a **fresh** runtime, insert another install line first: `!pip install -q openai` (many Colab images already include it).

---

### Cell 3 — Code — Imports

```python
import os
import requests
from IPython.display import Markdown, display, update_display
from openai import OpenAI
from google.colab import drive
from huggingface_hub import login
from google.colab import userdata
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
import torch
```

**Line by line:**

- `Markdown`, `display` — render markdown nicely in Colab output cells.
- `OpenAI` — client class for OpenAI’s HTTP APIs (used for transcription option).
- `drive` — mount Google Drive to read `denver_extract.mp3`.
- `userdata` — read Colab secrets.
- `login` — authenticate to Hugging Face Hub.
- `transformers` / `torch` — same Llama generation stack as Day 4.

**Unused import note:** `os` and `requests` may be unused in the minimal path—harmless leftovers or reserved for extensions.

---

### Cell 4 — Code — Model id constant

```python
LLAMA = "meta-llama/Llama-3.2-3B-Instruct"
```

**3B instruct** checkpoint—requires Meta license acceptance on the Hub; larger than Day 4’s 1B demo, so VRAM pressure is higher.

---

### Cell 5 — Code — Mount Drive + audio path

```python
drive.mount("/content/drive")
audio_filename = "/content/drive/MyDrive/llms/denver_extract.mp3"
```

**Line by line:**

- `drive.mount(...)` — opens an OAuth popup the first time; grants this notebook access to your Drive files.
- `audio_filename` — **must exist** at that path. Create folder `llms` under `MyDrive` and place the mp3 as instructed.

---

### Cell 6 — Markdown — Download reminder

Repeats the Drive link for `denver_extract.mp3`.

---

### Cell 7 — Code — Hugging Face login + open audio file

```python
hf_token = userdata.get('HF_TOKEN')
login(hf_token, add_to_git_credential=True)

audio_file = open(audio_filename, "rb")
```

**Line by line:**

- `open(..., "rb")` — binary read mode; APIs expect a **file-like object** with bytes for upload-style calls.

**Important:** The file handle `audio_file` is read later by OpenAI’s API. If you rewind or reuse, watch pointer position; for a simple linear notebook flow it is fine.

---

### Cell 8 — Markdown — STEP 1 heading

---

### Cell 9 — Markdown — Option 1 title

Open-source transcription with **Transformers `pipeline`**.

---

### Cell 10 — Code — Whisper pipeline (English medium)

```python
from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium.en",
    dtype=torch.float16,
    device='cuda',
    return_timestamps=True
)

result = pipe(audio_filename)
transcription = result["text"]
print(transcription)
```

**Line by line:**

- `"automatic-speech-recognition"` — ASR task tag.
- `model="openai/whisper-medium.en"` — English-focused Whisper **medium** checkpoint (balance of speed/accuracy).
- `dtype=torch.float16` — run math in half precision where supported to save memory.
- `device='cuda'` — GPU inference strongly recommended for medium Whisper.
- `return_timestamps=True` — include segment timing metadata inside `result` (even if only `text` is printed).
- `result["text"]` — full transcript string.

**Expected runtime:** May take noticeable minutes on a T4 for long audio.

---

### Cell 11 — Code — Save open-source transcript

```python
open_source_transcription = transcription
```

Preserves Option 1 output before Option 2 **overwrites** `transcription`.

---

### Cell 12 — Markdown — Option 2 title

Cloud API transcription with OpenAI.

---

### Cell 13 — Code — OpenAI transcription

```python
AUDIO_MODEL = "gpt-4o-mini-transcribe"

openai_api_key = userdata.get('OPENAI_API_KEY')
openai = OpenAI(api_key=openai_api_key)
transcription = openai.audio.transcriptions.create(model=AUDIO_MODEL, file=audio_file, response_format="text")
print(transcription)
```

**Line by line:**

- `AUDIO_MODEL` — string id for the transcription model on OpenAI’s side (course choice; may change—check OpenAI docs if deprecated).
- `userdata.get('OPENAI_API_KEY')` — Colab secret.
- `OpenAI(api_key=...)` — constructs a client object with auth header configuration.
- `audio.transcriptions.create(...)` — HTTP call under the hood; uploads audio bytes; returns an object whose string representation or `.text` accessor resolves to transcript text when `response_format="text"`.

**Billing note:** This call incurs **OpenAI usage charges** according to your account plan.

---

### Cell 14 — Code — Side-by-side markdown display

```python
display(Markdown(open_source_transcription))
print("\n\n")
display(Markdown(transcription))
```

Renders **both** transcripts as markdown for quick visual comparison (differences in punctuation, disfluencies, etc.).

---

### Cell 15 — Markdown — STEP 2 heading

---

### Cell 16 — Code — Build chat messages for minutes

```python
system_message = """
You produce minutes of meetings from transcripts, with summary, key discussion points,
takeaways and action items with owners, in markdown format without code blocks.
"""

user_prompt = f"""
Below is an extract transcript of a Denver council meeting.
Please write minutes in markdown without code blocks, including:
- a summary with attendees, location and date
- discussion points
- takeaways
- action items with owners

Transcription:
{transcription}
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
  ]
```

**Line by line:**

- **System message** — high-level style and output contract (markdown, no fenced code blocks).
- **User prompt** — embeds the **entire** transcript via an f-string; for very long audio this can exceed context limits—production apps **chunk** transcripts.
- `messages` — standard chat shape for `apply_chat_template` (see Day 3 guide).

---

### Cell 17 — Code — Quantization config (same as Day 4)

```python
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)
```

See **Cell 10 — Quantization configuration** in [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md) for field meanings.

---

### Cell 18 — Code — Tokenize + load + generate with streaming

```python
tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
streamer = TextStreamer(tokenizer)
model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto", quantization_config=quant_config)
outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)
```

**Line by line:**

- `apply_chat_template(..., return_tensors="pt")` — here **without** `add_generation_prompt=True` still works for many instruct models on single-turn user tasks, but if the model stalls or copies the prompt oddly, try adding `add_generation_prompt=True` (Day 4 lesson).
- `max_new_tokens=2000` — allows long minutes; increases time and risk of rambling—tune as needed.
- `streamer=streamer` — prints tokens live.

---

### Cell 19 — Code — Decode full tensor row

```python
response = tokenizer.decode(outputs[0])
```

Includes prompt + completion in one string; acceptable for a demo `display` step.

---

### Cell 20 — Code — Render model output as markdown

```python
display(Markdown(response))
```

If the model wrapped text in accidental code fences, markdown rendering would show them—your system prompt asked to avoid that.

---

### Cell 21 — Markdown — Student extension link

Points to an advanced Colab using **`TextIteratorStreamer`** + **Gradio**—optional.

---

### Cell 22 — Code — Empty

Ignore.

---

## Part C — Recap checklist

You should be able to:

- Compare **open-source ASR** (Whisper pipeline) vs **hosted ASR** (OpenAI) on the same audio file.
- Explain why `open_source_transcription` is saved **before** Option 2 runs.
- Walk through **messages → template → generate → decode → display** for Llama minutes.

---

## Part D — Common errors

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Drive mount fails | Popup blocked / wrong account | Retry mount; authorize |
| File not found | Wrong `audio_filename` path | Match folder layout `MyDrive/llms/...` |
| Whisper OOM | Medium model too big | Try a smaller Whisper checkpoint |
| OpenAI auth error | Missing `OPENAI_API_KEY` | Add secret |
| Llama 403 | Gated model | Accept license on Hub |

---

## Next guide

Optional extensions (image models, refiners, BFL): [11-generative-media-stable-diffusion-and-beyond.md](11-generative-media-stable-diffusion-and-beyond.md).
