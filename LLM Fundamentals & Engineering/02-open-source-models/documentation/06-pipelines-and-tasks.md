# Pipelines and Tasks

## What this guide is about

This guide explains one of the easiest ways to use open models in Python:
the Hugging Face `pipeline` function.

The goal is not only to show examples.
The goal is to help you understand what each example does and why it works.

## Step 1: What is a pipeline?

A pipeline is a ready-made function for a common AI task.

For example, a pipeline can be built for:

- sentiment analysis
- translation
- summarization
- text generation

The word `pipeline` here means:
"a helper that loads the right model and gives you a simple way to use it."

You create it once:

```python
my_pipeline = pipeline("task-name")
```

What this line means:

- `pipeline(...)` is a function from the `transformers` library.
- `"task-name"` is the task you want, such as `"sentiment-analysis"` or `"text-generation"`.
- `my_pipeline` is just a variable name. It stores the ready-to-use pipeline object.

Then you use it:

```python
result = my_pipeline("your input")
```

What this line means:

- `my_pipeline(...)` calls the pipeline like a normal Python function.
- `"your input"` is the text, image, or other input you want to send in.
- `result` stores the output so you can inspect it or print it later.

## Step 2: Basic setup

Before using pipelines, you usually install packages and log in to Hugging Face.

```python
!pip install -q --upgrade datasets==3.6.0 transformers==4.57.6 diffusers

from google.colab import userdata
from huggingface_hub import login
from transformers import pipeline

hf_token = userdata.get("HF_TOKEN")
login(hf_token, add_to_git_credential=True)
```

Before reading the lines, here are the key names:

- `pip` installs Python packages
- `userdata` reads saved secrets in Colab
- `login` connects your notebook to Hugging Face
- `pipeline` is the helper used in the rest of this guide

Line by line:

- `!pip install ...` runs a shell command inside the notebook.
- `datasets==3.6.0` installs one fixed version of the `datasets` library.
- `transformers==4.57.6` installs one fixed version of the `transformers` library.
- `diffusers` installs the library used later for image-generation pipelines.
- `-q` means quiet mode, so the output is shorter.
- `--upgrade` tells `pip` to update the package if an older version is already installed.
- `from google.colab import userdata` imports the Colab helper for reading secrets.
- `from huggingface_hub import login` imports the login function from Hugging Face.
- `from transformers import pipeline` imports the main helper used in this guide.
- `hf_token = userdata.get("HF_TOKEN")` reads the secret called `HF_TOKEN` and stores it in the variable `hf_token`.
- `login(hf_token, add_to_git_credential=True)` signs your notebook in to Hugging Face.
- `add_to_git_credential=True` tells the tool to store the token in a way that can help later authenticated downloads in the same environment.

If you plan to run image or audio examples, a GPU helps a lot.

## Step 3: Sentiment analysis

Sentiment analysis means deciding whether text sounds positive, negative, or neutral.

```python
sentiment = pipeline("sentiment-analysis", device="cuda")
result = sentiment("I'm super excited to be on the way to LLM mastery!")
print(result)
```

Before reading the lines:

- `pipeline` creates the task-specific helper
- `device="cuda"` tells the code to use an NVIDIA GPU

Line by line:

- `sentiment = pipeline("sentiment-analysis", device="cuda")` creates a sentiment-analysis pipeline and stores it in the variable `sentiment`.
- `"sentiment-analysis"` is the task name.
- `device="cuda"` means "run this on the GPU instead of the CPU."
- `result = sentiment("...")` sends one sentence into the pipeline.
- `print(result)` prints the output.

Example output from the course:

```text
[{'label': 'POSITIVE', 'score': 0.9993460774421692}]
```

What the output means:

- `label` is the predicted class
- `score` is the model's confidence-like value for that class

## Step 4: A second sentiment model

Sometimes you want to choose the exact model instead of using a default one.

```python
better_sentiment = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device="cuda",
)
result = better_sentiment("I should be more excited to be on the way to LLM mastery!!")
print(result)
```

Before reading the lines:

- `model="..."` is the model ID on Hugging Face
- a model ID tells Hugging Face exactly which saved model to load

Line by line:

- `better_sentiment = pipeline(...)` creates another sentiment pipeline.
- `"sentiment-analysis"` still tells the code which task you want.
- `model="nlptown/bert-base-multilingual-uncased-sentiment"` asks for one specific multilingual model instead of a default model.
- `device="cuda"` again asks to use the GPU.
- `result = better_sentiment("...")` runs the text through this new pipeline.
- `print(result)` shows the output.

Example output from the course:

```text
[{'label': '3 stars', 'score': 0.39448031783103943}]
```

This shows why model choice matters:
different models can use different label styles.

## Step 5: Named entity recognition

Named entity recognition, or NER, finds important names in text.
These names can be people, companies, places, and other categories.

```python
ner = pipeline("ner", device="cuda")
result = ner(
    "AI Engineers are learning about the amazing pipelines from HuggingFace in Google Colab from Ed Donner"
)
for entity in result:
    print(entity)
```

Before reading the lines:

- `ner` is just the variable name
- `"ner"` is the task name for named entity recognition

Line by line:

- `ner = pipeline("ner", device="cuda")` creates a NER pipeline.
- `result = ner(...)` sends one sentence into the NER pipeline.
- The long string is the sentence the model will inspect.
- `for entity in result:` loops through each found entity one by one.
- `print(entity)` prints each entity dictionary.

Short sample from the saved output:

```text
{'entity': 'I-ORG', 'word': 'AI', 'start': 0, 'end': 2}
{'entity': 'I-MISC', 'word': 'Google', 'start': 74, 'end': 80}
{'entity': 'I-PER', 'word': 'Ed', 'start': 92, 'end': 94}
```

What some output fields mean:

- `entity` is the predicted category
- `word` is the text piece the model found
- `start` and `end` show where that text appears in the sentence

## Step 6: Question answering

This task finds an answer inside a given text.

```python
question = "What are Hugging Face pipelines?"
context = "Pipelines are a high level API for inference of LLMs with common tasks"

qa = pipeline("question-answering", device="cuda")
result = qa(question=question, context=context)
print(result)
```

Before reading the lines:

- `question` is what you ask
- `context` is the text that contains the answer
- `qa` is a short variable name for the question-answering pipeline

Line by line:

- `question = "..."` stores the question.
- `context = "..."` stores the text the model is allowed to search.
- `qa = pipeline("question-answering", device="cuda")` creates a question-answering pipeline.
- `result = qa(question=question, context=context)` runs the task.
- `question=question` tells the pipeline which text is the question.
- `context=context` tells the pipeline which text contains the answer.
- `print(result)` prints the answer object.

Example output from the course:

```text
{'score': 0.24576981365680695, 'start': 35, 'end': 70, 'answer': 'inference of LLMs with common tasks'}
```

Here, `answer` is the selected span from the context.

## Step 7: Summarization

Summarization means turning a longer text into a shorter version.

```python
summarizer = pipeline("summarization", device="cuda")
text = """
The Hugging Face transformers library is an incredibly versatile and powerful tool for natural language processing.
It allows users to perform a wide range of tasks such as text classification, named entity recognition, and question answering.
It is widely used by the open-source data science community.
"""

summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print(summary[0]["summary_text"])
```

Before reading the lines:

- `summarizer` is the pipeline variable
- `max_length` and `min_length` control output size
- `do_sample=False` asks for a more predictable result

Line by line:

- `summarizer = pipeline("summarization", device="cuda")` creates a summarization pipeline.
- `text = """..."""` stores a multi-line text string.
- `summary = summarizer(...)` runs the summarizer on that text.
- `max_length=50` tells the model not to make the summary too long.
- `min_length=25` asks the model not to make it too short.
- `do_sample=False` reduces randomness and makes the result more stable.
- `print(summary[0]["summary_text"])` prints the summary text from the first result item.

Example output from the course:

```text
The Hugging Face transformers library is an incredibly versatile and powerful tool for natural language processing . It allows users to perform a wide range of tasks such as text classification, named entity recognition, and question answering .
```

## Step 8: Translation

Translation changes text from one language to another.

French example:

```python
translator = pipeline("translation_en_to_fr", device="cuda")
result = translator(
    "The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API."
)
print(result[0]["translation_text"])
```

Line by line:

- `translator = pipeline("translation_en_to_fr", device="cuda")` creates a translation pipeline from English to French.
- `"translation_en_to_fr"` is the task name.
- `result = translator("...")` sends one English sentence to the pipeline.
- `print(result[0]["translation_text"])` prints the translated text from the first result item.

Example output from the course:

```text
Les Data Scientists ont été vraiment étonnés par la puissance et la simplicité de l'API du pipeline HuggingFace.
```

Spanish example with a fixed model:

```python
translator = pipeline(
    "translation_en_to_es",
    model="Helsinki-NLP/opus-mt-en-es",
    device="cuda",
)
result = translator(
    "The Data Scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API."
)
print(result[0]["translation_text"])
```

Line by line:

- `translator = pipeline(...)` creates another translation pipeline.
- `"translation_en_to_es"` means English to Spanish.
- `model="Helsinki-NLP/opus-mt-en-es"` picks one exact translation model.
- `device="cuda"` asks for GPU use again.
- `result = translator("...")` runs the translation.
- `print(result[0]["translation_text"])` prints the Spanish output.

Example output from the course:

```text
Los científicos de datos estaban verdaderamente sorprendidos por el poder y la simplicidad de la API de tuberías HuggingFace.
```

## Step 9: Other useful text tasks

You can use the same pipeline pattern for many other tasks.

```python
classifier = pipeline("zero-shot-classification", device="cuda")
generator = pipeline("text-generation", device="cuda")
```

Line by line:

- `classifier = pipeline("zero-shot-classification", device="cuda")` creates a pipeline that can score text against labels you provide.
- `"zero-shot-classification"` means the model can work with your labels even if it was not trained only on those exact labels.
- `generator = pipeline("text-generation", device="cuda")` creates a text-generation pipeline.
- `"text-generation"` means the model will continue text from a prompt.

Typical results:

- zero-shot classification returns labels and scores
- text generation returns the prompt plus the new generated text

## Step 10: Text-to-image

This example uses a different library called `diffusers`.
`AutoPipelineForText2Image` is a class that loads the correct image-generation pipeline for the model you choose.

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

- `from IPython.display import display` imports the helper that can show images inside the notebook.
- `from diffusers import AutoPipelineForText2Image` imports the class used for text-to-image pipelines.
- `import torch` imports PyTorch.
- `pipe = AutoPipelineForText2Image.from_pretrained(...)` loads a saved image model from Hugging Face.
- `from_pretrained(...)` is a Hugging Face method that downloads and prepares saved model files.
- `"stabilityai/sdxl-turbo"` is the model ID.
- `torch_dtype=torch.float16` asks the model to use a smaller 16-bit number format to save memory.
- `variant="fp16"` asks for the fp16 version of the model files when available.
- `pipe.to("cuda")` moves the pipeline to the GPU.
- `image = pipe(...)` runs the pipeline.
- `prompt="..."` is the text description of the image you want.
- `num_inference_steps=4` tells the model how many denoising steps to use.
- `guidance_scale=0.0` controls how strongly the image follows the prompt.
- `.images[0]` takes the first image from the result.
- `display(image)` shows the image in the notebook.

Output:

```text
An image is shown inside Colab.
```

## Step 11: Text-to-speech

This example uses a speech model.
`load_dataset` is a helper from the `datasets` library.
It downloads a dataset in a standard way.

```python
from datasets import load_dataset
import torch
from IPython.display import Audio

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device="cuda")
embeddings_dataset = load_dataset(
    "matthijs/cmu-arctic-xvectors",
    split="validation",
    trust_remote_code=True,
)
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
speech = synthesiser(
    "Hi to an artificial intelligence engineer, on the way to mastery!",
    forward_params={"speaker_embeddings": speaker_embedding},
)

Audio(speech["audio"], rate=speech["sampling_rate"])
```

Line by line:

- `from datasets import load_dataset` imports the dataset-loading function.
- `import torch` imports PyTorch.
- `from IPython.display import Audio` imports the helper that can show an audio player in the notebook.
- `synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device="cuda")` creates a text-to-speech pipeline.
- `"text-to-speech"` is the task name.
- `"microsoft/speecht5_tts"` is the exact model ID.
- `device="cuda"` asks for GPU use.
- `embeddings_dataset = load_dataset(...)` downloads a dataset of speaker embeddings.
- `"matthijs/cmu-arctic-xvectors"` is the dataset ID.
- `split="validation"` selects the validation part of that dataset.
- `trust_remote_code=True` allows dataset-specific loading code from the source. Use this only when you trust the dataset source.
- `speaker_embedding = torch.tensor(...).unsqueeze(0)` turns one speaker vector into a PyTorch tensor and adds a batch dimension.
- `embeddings_dataset[7306]["xvector"]` selects one example speaker embedding from the dataset.
- `speech = synthesiser(...)` creates speech audio from the text.
- `forward_params={"speaker_embeddings": speaker_embedding}` sends the chosen voice embedding into the model.
- `Audio(speech["audio"], rate=speech["sampling_rate"])` shows an audio player using the waveform and sample rate returned by the model.

Output:

```text
An audio player is shown inside Colab.
```

## What to remember

- A pipeline is a simple way to run a common model task.
- The task name tells Hugging Face what kind of pipeline to build.
- A model ID lets you choose one exact model instead of a default one.
- The same pattern works for text, images, and audio.
- Understanding the parameters helps you move from copying code to really using it.
