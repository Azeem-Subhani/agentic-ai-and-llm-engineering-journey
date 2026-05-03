# Open Source Models — Course Documentation

This folder turns the raw class notes ([`../notes.md`](../notes.md)) into structured, beginner-friendly guides. Each guide builds ideas in order and defines new words before relying on them.

## Who this is for

You can read these documents **without** having built machine learning systems before. When we use Python or cloud tools, we say what they are for and what you should click or type.

## How this folder relates to the notebooks

The course uses four Jupyter notebooks (exported from Google Colab). They live next to this folder:

| Notebook | Topic |
|----------|--------|
| [`../week_3_day_2_pipelines.ipynb`](../week_3_day_2_pipelines.ipynb) | High-level Hugging Face `pipeline` API: NLP tasks, image, and speech |
| [`../Week_3_Day_3_tokenizers.ipynb`](../Week_3_Day_3_tokenizers.ipynb) | Tokenizers, token IDs, chat templates, comparing models |
| [`../Week_3_Day_4_models.ipynb`](../Week_3_Day_4_models.ipynb) | Loading causal LMs, 4-bit quantization, `generate`, streaming |
| [`../Week_3_Day_5_Meeting_Minutes_product.ipynb`](../Week_3_Day_5_Meeting_Minutes_product.ipynb) | Audio → transcript → meeting minutes with Whisper or OpenAI |

**Suggested order:** Read guides `01`–`05` first (concepts), then `06` while you run Day 2, `07` with Day 3, `08`–`09` with Day 4, `10` with Day 5. Finish with `11` for optional extension topics.

## Reading order (all guides)

1. [01-what-are-open-source-models.md](01-what-are-open-source-models.md)
2. [02-pytorch-and-tensorflow.md](02-pytorch-and-tensorflow.md)
3. [03-hugging-face-ecosystem.md](03-hugging-face-ecosystem.md)
4. [04-ollama-vs-hugging-face-workflows.md](04-ollama-vs-hugging-face-workflows.md)
5. [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md)
6. [06-pipelines-and-tasks.md](06-pipelines-and-tasks.md) — walkthrough: `week_3_day_2_pipelines.ipynb`
7. [07-tokens-and-tokenizers.md](07-tokens-and-tokenizers.md) — walkthrough: `Week_3_Day_3_tokenizers.ipynb`
8. [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md) — walkthrough: `Week_3_Day_4_models.ipynb`
9. [09-inside-llama-decoder-architecture.md](09-inside-llama-decoder-architecture.md)
10. [10-meeting-minutes-audio-product.md](10-meeting-minutes-audio-product.md) — walkthrough: `Week_3_Day_5_Meeting_Minutes_product.ipynb`
11. [11-generative-media-stable-diffusion-and-beyond.md](11-generative-media-stable-diffusion-and-beyond.md) — extension (no matching notebook in this repo)

## Running the notebooks safely

### Hugging Face token (required for most cells)

1. Create a free account at [https://huggingface.co](https://huggingface.co).
2. **Settings → Access Tokens** → create a token. The course notebooks ask for **read/write** access (select the **Write** scope when creating the token).
3. In Google Colab: click the **key** icon in the left sidebar → add a secret named `HF_TOKEN` with your token value → enable notebook access to that secret.

### OpenAI key (only for Day 5, Option 2)

Add a Colab secret `OPENAI_API_KEY` if you run the OpenAI transcription path in the meeting-minutes notebook.

### Gated models (Llama, Gemma, …)

Some model pages on the Hub require you to **accept a license** on the model card *before* `from_pretrained` works. Visit the model URL in the notebook, click to agree, wait until the page shows you have access, then rerun the download cells.

### GPU runtime and the “CUDA / bitsandbytes” confusion

The notebooks include a **pro-tip**: if you see an error like “CUDA is required but not available for bitsandbytes,” it often means Colab **reassigned you to a CPU-only runtime**, not that your package versions are wrong. Fix:

1. **Kernel → Disconnect and delete runtime**
2. Reload the notebook, **Edit → Clear all outputs**
3. Connect to a **GPU** runtime again (e.g. T4) and confirm under **View resources**
4. Rerun from the top, starting with `pip install` cells

### Paid accelerators (A100, etc.)

If you start a **paid** high-end GPU session, **terminate or disconnect** when you are done so you are not billed for idle time.

### Secrets and git

Never commit API keys or tokens into git. The notebooks read secrets from the Colab environment, not from hard-coded strings in files you push to GitHub.

## Glossary (quick reference)

| Term | One-line meaning |
|------|------------------|
| **Inference** | Using a model that is already trained to produce outputs on new inputs (not updating its weights). |
| **Training** | Showing the model data and updating its internal weights so it improves at a task. |
| **Token** | A small piece of text (often a subword) that the model sees as one symbol from a fixed vocabulary. |
| **Tokenizer** | Code that splits text into tokens and maps each token to an integer **token ID**. |
| **Pipeline (HF)** | A high-level function that loads a sensible default model for a named task and runs inference. |
| **Hub** | Hugging Face’s website and storage where models, datasets, and spaces are shared. |
| **Quantization** | Storing or computing weights with fewer bits than full precision to save memory. |
| **Causal language model** | A model that predicts the next token given all previous tokens (typical “GPT-style” text model). |
| **ASR** | Automatic Speech Recognition: audio → text (e.g. Whisper). |
| **Gated model** | A Hub model that requires accepting a license before download works. |
| **Context window** | Maximum number of tokens (prompt + completion) a model can attend to at once—long transcripts may need chunking. |
| **bitsandbytes** | Library used with Hugging Face to load some models in 4-bit quantized form on GPU. |

For fuller definitions, see guides `01`–`09` and walkthroughs `06`–`10`.

## Common mistakes (quick triage)

| Symptom | First thing to check |
|---------|----------------------|
| `CUDA` / `bitsandbytes` errors right after things worked | Colab switched you to **CPU** — use the disconnect/runtime checklist in [05-google-colab-and-gpus.md](05-google-colab-and-gpus.md). |
| `403` when calling `from_pretrained` | **Gated model:** accept license on the model card; confirm `HF_TOKEN` has access. |
| `401` / invalid token | Colab secret missing, typo, or expired Hub token. |
| OpenAI errors on Day 5 | `OPENAI_API_KEY` secret; billing; model name still valid in OpenAI docs. |
| `FileNotFoundError` for audio | Google Drive path must match `MyDrive/llms/denver_extract.mp3` (or your chosen path). |
| Out of memory on image or Llama cells | Smaller model id, fewer `max_new_tokens`, enable 4-bit quant, or restart runtime after `del` + `empty_cache`. |

## Original class notes

The unedited bullet list the class started from is still at [`../notes.md`](../notes.md).
