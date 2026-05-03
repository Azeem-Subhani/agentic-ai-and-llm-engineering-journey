# Tokens and Tokenizers

## What this guide is about

This guide explains how text becomes numbers before a model can use it.

That process is very important because models do not read raw text directly.
They read token IDs.

This page also explains the code used to load and use tokenizers in simple steps.

## Step 1: What is a token?

A token is a small piece of text that a model reads as one unit.

A token can be:

- a whole word
- part of a word
- punctuation
- a special marker

That is why one sentence can have:

- a character count
- a word count
- a token count

and all three can be different.

## Step 2: What is a tokenizer?

A tokenizer is the tool that changes text into token IDs.

It usually does two jobs:

1. split text into tokens
2. turn those tokens into numbers

It can also do the reverse and turn token IDs back into text.

## Step 3: What is a vocabulary?

A vocabulary is the list of tokens a tokenizer knows.
Each token in the vocabulary has an ID.

If the tokenizer does not know a whole word, it may split that word into smaller pieces that do exist in the vocabulary.

## Step 4: What is a special token?

A special token is a token with a special meaning.

Examples include tokens that mark:

- the start of text
- the end of text
- the start of a user message
- the start of an assistant reply

These tokens help the model understand structure, not only words.

## Step 5: Basic setup

Before the code, here are the important names:

- `AutoTokenizer` is a Hugging Face class that picks the correct tokenizer class for the model you name
- `from_pretrained(...)` is a common Hugging Face method that downloads saved files and prepares them for use

```python
!pip install -q --upgrade datasets==3.6.0 transformers==4.57.6

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B",
    trust_remote_code=True,
)
```

Line by line:

- `!pip install -q --upgrade datasets==3.6.0 transformers==4.57.6` installs the package versions used in this guide.
- `from transformers import AutoTokenizer` imports the `AutoTokenizer` class from the `transformers` library.
- `tokenizer = AutoTokenizer.from_pretrained(...)` loads a tokenizer and stores it in the variable `tokenizer`.
- `"meta-llama/Meta-Llama-3.1-8B"` is the model ID on Hugging Face. It tells the code which tokenizer files to load.
- `trust_remote_code=True` allows model-specific code from the source to run if the tokenizer needs it. Use this only when you trust the model source.

Some models require you to accept a license on Hugging Face first.

## Step 6: Encode text

The method `encode(...)` turns text into token IDs.

```python
text = "I am excited to show Tokenizers in action to my LLM engineers"
tokens = tokenizer.encode(text)
print(tokens)
```

Line by line:

- `text = "..."` stores the sentence in a variable called `text`.
- `tokens = tokenizer.encode(text)` asks the tokenizer to turn that sentence into token IDs.
- `encode(...)` is a tokenizer method for text-to-IDs conversion.
- `print(tokens)` prints the list of token IDs.

Example output shape:

```text
[... a list of integer token IDs ...]
```

The exact numbers change from one model to another.

## Step 7: Decode text

The method `decode(...)` turns token IDs back into text.

```python
print(tokenizer.decode(tokens))
```

Line by line:

- `tokenizer.decode(tokens)` asks the tokenizer to turn the list of token IDs back into text.
- `tokens` is the list created in the earlier step.
- `print(...)` shows the result.

Expected result:

```text
I am excited to show Tokenizers in action to my LLM engineers
```

## Step 8: Tokens are not words

```python
character_count = len(text)
word_count = len(text.split(" "))
print(character_count, word_count)
```

Before reading the lines:

- `len(...)` returns the size of something
- `split(" ")` splits the sentence at spaces

Line by line:

- `character_count = len(text)` counts how many characters are in the full string.
- `word_count = len(text.split(" "))` splits the sentence into pieces at spaces and then counts them.
- `print(character_count, word_count)` prints the two counts.

For this sentence:

```text
61 12
```

The token count will be different again.
This is why token limits and word counts are not the same thing.

## Step 9: Look at vocabulary information

```python
print(tokenizer.get_added_vocab())
print(len(tokenizer.vocab))
```

Before reading the lines:

- `get_added_vocab()` shows tokens added on top of the base vocabulary
- `tokenizer.vocab` is the vocabulary object

Line by line:

- `print(tokenizer.get_added_vocab())` prints the extra tokens the tokenizer added.
- `print(len(tokenizer.vocab))` prints the size of the vocabulary.

This shows:

- extra tokens added by the tokenizer
- the size of the vocabulary

## Step 10: Instruct models and chat templates

Some models are trained for chat.
These are often called instruct models.

A chat model usually expects the prompt in a special format.
That format is often built with a chat template.

Before the code, here are the important names:

- `apply_chat_template(...)` is a tokenizer method that turns a message list into the prompt style the model expects
- `tokenize=False` means "return text, not token IDs yet"
- `add_generation_prompt=True` means "add the marker that tells the model the assistant reply should start now"

```python
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    trust_remote_code=True,
)

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"},
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

print(prompt)
```

Line by line:

- `tokenizer = AutoTokenizer.from_pretrained(...)` loads the tokenizer for the instruct version of the model.
- `"meta-llama/Meta-Llama-3.1-8B-Instruct"` is the model ID for the instruct model.
- `messages = [...]` creates a list of chat messages.
- Each message is a dictionary with a `role` and `content`.
- `"system"` is usually used for high-level instructions.
- `"user"` is usually used for the user's input.
- `prompt = tokenizer.apply_chat_template(...)` converts the message list into one formatted prompt string.
- `messages` is the message list that will be formatted.
- `tokenize=False` asks for plain text output instead of token IDs.
- `add_generation_prompt=True` adds the assistant-start marker so the model knows it should answer next.
- `print(prompt)` prints the full formatted prompt.

Example output idea:

```text
... special markers for system ...
You are a helpful assistant
... special markers for user ...
Tell a light-hearted joke for a room of Data Scientists
... special markers for assistant ...
```

The exact markers depend on the model family.

## Step 11: Why chat templates matter

Your Python app may store messages as dictionaries.
The model does not read dictionaries.

The flow is:

1. messages
2. one formatted text prompt
3. tokens
4. token IDs

That is the bridge between app code and model input.

## Step 12: Different models tokenize differently

The same sentence can become different token IDs with different models.

```python
PHI4 = "microsoft/Phi-4-mini-instruct"
DEEPSEEK = "deepseek-ai/DeepSeek-V3.1"

phi4_tokenizer = AutoTokenizer.from_pretrained(PHI4)
deepseek_tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK)

print(tokenizer.encode(text))
print(phi4_tokenizer.encode(text))
print(deepseek_tokenizer.encode(text))
```

Line by line:

- `PHI4 = "microsoft/Phi-4-mini-instruct"` stores the model ID for a Phi tokenizer.
- `DEEPSEEK = "deepseek-ai/DeepSeek-V3.1"` stores the model ID for a DeepSeek tokenizer.
- `phi4_tokenizer = AutoTokenizer.from_pretrained(PHI4)` loads the Phi tokenizer.
- `deepseek_tokenizer = AutoTokenizer.from_pretrained(DEEPSEEK)` loads the DeepSeek tokenizer.
- `print(tokenizer.encode(text))` prints token IDs from the current tokenizer.
- `print(phi4_tokenizer.encode(text))` prints token IDs from the Phi tokenizer.
- `print(deepseek_tokenizer.encode(text))` prints token IDs from the DeepSeek tokenizer.

Expected result:

```text
Three different lists of token IDs
```

This is normal because different model families often use different vocabularies and token rules.

## Step 13: Different chat templates too

The same `messages` list can also become different prompt text across models.

```python
print(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
print(phi4_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
```

Line by line:

- The first line prints the chat template output for the current tokenizer.
- The second line prints the chat template output for the Phi tokenizer.
- `tokenize=False` again asks for plain text.
- `add_generation_prompt=True` again asks to add the assistant-start marker.

This is why chat code that works for one model may need a different template for another.

## Step 14: Tokenizing code

Some models are trained especially for code.

```python
QWEN_CODER = "Qwen/Qwen2.5-Coder-7B-Instruct"
qwen_tokenizer = AutoTokenizer.from_pretrained(QWEN_CODER)

code = '''
def hello_world(person):
  print("Hello", person)
'''

tokens = qwen_tokenizer.encode(code)
for token in tokens:
    print(token, qwen_tokenizer.decode([token]))
```

Line by line:

- `QWEN_CODER = "Qwen/Qwen2.5-Coder-7B-Instruct"` stores the model ID for a code-focused tokenizer.
- `qwen_tokenizer = AutoTokenizer.from_pretrained(QWEN_CODER)` loads that tokenizer.
- `code = '''...'''` stores a short Python function in a multi-line string.
- `tokens = qwen_tokenizer.encode(code)` converts the code into token IDs.
- `for token in tokens:` loops through the token IDs one by one.
- `qwen_tokenizer.decode([token])` decodes one token ID at a time so you can see what text piece it maps to.
- `print(token, ...)` prints the token ID and its decoded text piece together.

This helps you see how code models split indentation, names, brackets, and symbols.

## What to remember

- Models read token IDs, not raw text.
- `AutoTokenizer` loads the correct tokenizer for a model ID.
- `from_pretrained(...)` loads saved tokenizer files.
- `encode(...)` turns text into token IDs.
- `decode(...)` turns token IDs back into text.
- Chat templates are important because instruct models expect a special prompt format.
