# Meeting Minutes from Audio

## What this guide is about

This guide shows a small end-to-end AI product:

1. take audio
2. turn it into text
3. turn that text into meeting minutes

The code uses two kinds of models:

- a speech-to-text model
- a chat model for writing the final report

The main goal of this page is to explain not only what the code does, but also why each part is used.

## Step 1: What are we building?

This mini-project turns speech into meeting minutes.

The flow is:

1. audio
2. transcription
3. summary and action items

Transcription means changing speech into text.

## Step 2: Install and import

Before the code, here are the important names:

- `OpenAI` is the Python client class for OpenAI API calls
- `drive` is the Colab helper for Google Drive
- `userdata` reads saved secrets in Colab
- `pipeline` is the Hugging Face helper for common tasks
- `Markdown` and `display` show nicely formatted output in the notebook

```python
!pip install -q --upgrade bitsandbytes accelerate transformers==4.57.6 openai

from openai import OpenAI
from google.colab import drive, userdata
from huggingface_hub import login
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TextStreamer,
    pipeline,
)
from IPython.display import Markdown, display
import torch
```

Line by line:

- `!pip install ...` installs the packages needed for the model-loading steps in this project.
- `bitsandbytes` helps with 4-bit model loading.
- `accelerate` helps with device placement for larger models.
- `transformers==4.57.6` installs the `transformers` library version used in these examples.
- `openai` installs the OpenAI Python package used in the paid transcription option.
- `from openai import OpenAI` imports the OpenAI client class.
- `from google.colab import drive, userdata` imports the Drive helper and the Colab secrets helper.
- `from huggingface_hub import login` imports the Hugging Face login function.
- `from transformers import (...)` imports the Hugging Face classes used later.
- `AutoTokenizer` loads the tokenizer for a model.
- `AutoModelForCausalLM` loads a chat-style text model.
- `BitsAndBytesConfig` stores quantization settings.
- `TextStreamer` prints generated tokens as they appear.
- `pipeline` creates a ready-made task helper such as speech recognition.
- `from IPython.display import Markdown, display` imports tools for showing Markdown nicely in the notebook.
- `import torch` imports PyTorch.

You need:

- `HF_TOKEN` for Hugging Face
- `OPENAI_API_KEY` only if you use the OpenAI transcription option

Log in before loading gated models:

```python
login(userdata.get("HF_TOKEN"), add_to_git_credential=True)
```

Line by line:

- `userdata.get("HF_TOKEN")` reads the Hugging Face token from Colab secrets.
- `login(...)` signs the notebook in to Hugging Face.
- `add_to_git_credential=True` helps later authenticated downloads in the same environment.

## Step 3: Connect Google Drive

```python
drive.mount("/content/drive")
audio_filename = "/content/drive/MyDrive/llms/denver_extract.mp3"
audio_file = open(audio_filename, "rb")
```

Before reading the lines:

- `drive.mount(...)` connects your notebook to your Google Drive
- `open(..., "rb")` opens a file in binary read mode

Line by line:

- `drive.mount("/content/drive")` connects Google Drive to the notebook.
- `"/content/drive"` is the path where Drive will appear inside Colab.
- `audio_filename = "..."` stores the full file path of the audio file.
- `audio_file = open(audio_filename, "rb")` opens that audio file for reading.
- `"rb"` means read binary, which is the correct mode for an audio file sent to an API.

The old notebook used a Denver City Council audio clip, but you can use your own audio file too.

## Step 4: Option 1, transcribe with Whisper

Before the code, here are the important names:

- `pipeline(...)` builds the speech-recognition helper
- `"automatic-speech-recognition"` is the task name
- `result["text"]` takes the plain transcript text from the output

```python
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium.en",
    dtype=torch.float16,
    device="cuda",
    return_timestamps=True,
)

result = pipe(audio_filename)
transcription = result["text"]
print(transcription)
```

Line by line:

- `pipe = pipeline(...)` creates the speech-recognition pipeline.
- `"automatic-speech-recognition"` is the task name for speech-to-text.
- `model="openai/whisper-medium.en"` picks the Whisper English model to use.
- `dtype=torch.float16` asks the model to use 16-bit floating-point numbers, which often saves GPU memory.
- `device="cuda"` asks to run on the GPU.
- `return_timestamps=True` asks the model to include timing information in the full result object.
- `result = pipe(audio_filename)` sends the audio file path into the pipeline.
- `transcription = result["text"]` takes only the transcript text from the full result dictionary.
- `print(transcription)` prints the transcript.

This is the open-source transcription path.

## Step 5: Option 2, transcribe with OpenAI

Before the code, here are the important names:

- `OpenAI(...)` creates the API client
- `audio.transcriptions.create(...)` sends the audio file to the transcription API

```python
AUDIO_MODEL = "gpt-4o-mini-transcribe"

openai = OpenAI(api_key=userdata.get("OPENAI_API_KEY"))
transcription = openai.audio.transcriptions.create(
    model=AUDIO_MODEL,
    file=audio_file,
    response_format="text",
)
print(transcription)
```

Line by line:

- `AUDIO_MODEL = "gpt-4o-mini-transcribe"` stores the transcription model name in a variable.
- `openai = OpenAI(api_key=userdata.get("OPENAI_API_KEY"))` creates the OpenAI client.
- `userdata.get("OPENAI_API_KEY")` reads the API key from Colab secrets.
- `transcription = openai.audio.transcriptions.create(...)` sends the audio file to the transcription API.
- `model=AUDIO_MODEL` tells the API which transcription model to use.
- `file=audio_file` sends the opened audio file.
- `response_format="text"` asks for plain text output instead of a more complex structure.
- `print(transcription)` prints the transcription result.

This path uses a paid API.

## Step 6: Build the meeting-minutes prompt

Before the code, here are the important names:

- `system_message` gives high-level instructions to the chat model
- `user_prompt` gives the task and the transcript
- `messages` stores the chat in the role/content format used by many model APIs

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
    {"role": "user", "content": user_prompt},
]
```

Line by line:

- `system_message = """..."""` stores the main behavior instructions for the model.
- The system message says what kind of output we want and how it should be formatted.
- `user_prompt = f"""..."""` stores the user's task request.
- The `f` before the string means it is an f-string, so Python can insert variable values into it.
- `{transcription}` inserts the transcript text into the prompt.
- `messages = [...]` creates the chat message list.
- `{"role": "system", "content": system_message}` adds the system instruction.
- `{"role": "user", "content": user_prompt}` adds the user request and transcript.

## Step 7: Load a Llama model

Before the code, here are the important names:

- `AutoTokenizer` loads the correct tokenizer for the model ID
- `AutoModelForCausalLM` loads the chat model
- `BitsAndBytesConfig` stores quantization settings
- `TextStreamer` prints output as it is generated

```python
LLAMA = "meta-llama/Llama-3.2-3B-Instruct"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
)

tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token
inputs = tokenizer.apply_chat_template(
    messages,
    return_tensors="pt",
    add_generation_prompt=True,
).to("cuda")

streamer = TextStreamer(tokenizer)
model = AutoModelForCausalLM.from_pretrained(
    LLAMA,
    device_map="auto",
    quantization_config=quant_config,
)
outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)
```

Line by line:

- `LLAMA = "meta-llama/Llama-3.2-3B-Instruct"` stores the model ID for the chat model.
- `quant_config = BitsAndBytesConfig(...)` creates the 4-bit quantization settings object.
- `load_in_4bit=True` asks for 4-bit model weights.
- `bnb_4bit_use_double_quant=True` asks for extra memory saving.
- `bnb_4bit_compute_dtype=torch.bfloat16` asks some calculations to use `bfloat16`.
- `bnb_4bit_quant_type="nf4"` selects the NF4 weight format.
- `tokenizer = AutoTokenizer.from_pretrained(LLAMA)` loads the tokenizer for the Llama model.
- `from_pretrained(...)` is the Hugging Face method that loads saved files for a model or tokenizer.
- `tokenizer.pad_token = tokenizer.eos_token` sets the padding token to be the same as the end-of-sequence token.
- `inputs = tokenizer.apply_chat_template(...)` formats the chat messages and turns them into token IDs.
- `messages` is the message list created earlier.
- `return_tensors="pt"` asks for a PyTorch tensor.
- `add_generation_prompt=True` adds the assistant-start marker so the model knows it should reply next.
- `.to("cuda")` moves the token tensor to the GPU.
- `streamer = TextStreamer(tokenizer)` creates the streamer that will print new tokens as they appear.
- `model = AutoModelForCausalLM.from_pretrained(...)` loads the chat model.
- `device_map="auto"` lets the library choose device placement.
- `quantization_config=quant_config` applies the 4-bit settings from earlier.
- `outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)` asks the model to generate the meeting minutes.
- `inputs` is the tokenized prompt.
- `max_new_tokens=2000` allows a long response.
- `streamer=streamer` prints the response as it is being generated.

## Step 8: Show the result

```python
response = tokenizer.decode(outputs[0])
display(Markdown(response))
```

Before reading the lines:

- `decode(...)` turns token IDs back into text
- `Markdown(...)` tells the notebook to render the text as Markdown

Line by line:

- `response = tokenizer.decode(outputs[0])` turns the first generated token sequence back into a text string.
- `outputs[0]` means "take the first output row."
- `display(Markdown(response))` renders the text as Markdown in the notebook.

Example output format:

```md
## Summary
Short overview of the meeting

## Discussion Points
- Main topic one
- Main topic two

## Takeaways
- Key lesson or decision

## Action Items
- Owner: task
```

## Step 9: Important practical note

Long transcripts can be too large for one prompt.
In a bigger project, you may need to split the transcript into smaller chunks first.

## What to remember

- First turn audio into text.
- Then turn text into structured minutes.
- `pipeline(...)` is the simple path for open-source transcription.
- `OpenAI(...)` is the client used for the API transcription path.
- `AutoTokenizer` and `AutoModelForCausalLM` are used for the final report-writing model.
- Understanding each parameter helps you adapt the project for your own audio later.
