# Generative Media — Extension Topics

## Status of this document

**This file is an extension.** Your class notes asked for more Colab examples around **Stable Diffusion**, **refiners**, **audio generation**, and **Black Forest Labs (BFL)** image models. Those topics are **partially demonstrated** inside [`../week_3_day_2_pipelines.ipynb`](../week_3_day_2_pipelines.ipynb) (SDXL Turbo + SpeechT5), but there is **no separate dedicated notebook** in this repository for every bullet in `notes.md`.

Treat everything below as **curriculum-aligned background** plus **pointers to official docs**—not a claim that a missing Colab exists line-for-line.

---

## Part A — What you already ran in class (cross-reference)

### Text-to-image (SDXL Turbo)

The Day 2 pipelines notebook uses **`diffusers.AutoPipelineForText2Image`** with **`stabilityai/sdxl-turbo`**. For a full walkthrough of that exact cell, open [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md) and scroll to **Cell 19 — Text-to-image (SDXL Turbo)**.

### Text-to-speech (audio generation)

The same notebook includes a **`pipeline("text-to-speech", "microsoft/speecht5_tts", ...)`** example with a **speaker embedding** from `datasets`. See **Cell 20** in [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md).

---

## Part B — Stable Diffusion family (concepts)

### What is a diffusion model?

Instead of predicting the next **word**, a **diffusion** image model starts from **noise** and repeatedly **denoises** a canvas until a picture emerges, conditioned on your **text prompt** (and sometimes other inputs).

**Stable Diffusion** is a family of open-weight image models popularized by Stability AI and the broader community. **SDXL** is a larger, higher-quality line within that family; **Turbo** variants are distilled for **very few steps** (fast previews).

### What is a “refiner”?

In SDXL workflows, a **base** model may draft the image, then a **refiner** model (another checkpoint) performs **extra denoising steps** focused on **details** (faces, textures). Practically:

- You run **two** staged pipelines or a combined API that hands latents from base → refiner.
- You trade **compute time** for **visual polish**.

Hugging Face `diffusers` documents combined base+refiner patterns in their SDXL guides—search the Diffusers documentation for “refiner” alongside “SDXL”.

---

## Part C — Black Forest Labs (BFL) and Flux

**Black Forest Labs** released the **Flux** family of image models (strong text rendering and realism at release time). From an engineering perspective, using Flux looks like:

1. Pick a **Hub model id** (if weights are hosted on Hugging Face) or follow BFL’s own hosting/API terms.  
2. Use **`diffusers`** (or the vendor’s SDK) with the matching pipeline class and dtype rules (often `bfloat16` / `float16` on GPU).  
3. Respect the **license** (commercial use may differ per checkpoint).

Because checkpoints and recommended APIs evolve quickly, the stable learning path is: **read the model card on the Hub** for the exact `from_pretrained` snippet rather than copying a stale blog command.

---

## Part D — Practical patterns (no magic URLs)

### Pattern 1 — Minimal text-to-image in Python

Conceptually (pseudo-outline, not pinned versions):

```python
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "MODEL_ID_ON_HUB",
    torch_dtype=torch.float16,
)
pipe.to("cuda")
image = pipe("your prompt here").images[0]
image.save("out.png")
```

**Beginner pitfalls:** CUDA OOM, missing `pip install diffusers`, gated models requiring HF login.

### Pattern 2 — Audio music vs speech

- **Text-to-speech** (what SpeechT5 does) maps text → **spoken waveform**.  
- **Text-to-music** or **instrumental generation** uses different model families (not interchangeable APIs).

Always read the **task tag** on the model card (`text-to-speech`, `text-to-audio`, etc.).

---

## Part E — How to extend this repo responsibly

If you add future notebooks:

1. Place `.ipynb` next to the Week 3 files (or under `documentation/notebooks/`).  
2. Add one row to [README.md](README.md)’s notebook table.  
3. Either expand this file or add `12-...md` with a true cell-by-cell walkthrough.

---

## Part F — Where to go next in this documentation set

- Core HF stack refresher: [03-hugging-face-ecosystem.md](03-hugging-face-ecosystem.md)  
- Colab + GPU hygiene: [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md)  
- Return to the main index: [README.md](README.md)
