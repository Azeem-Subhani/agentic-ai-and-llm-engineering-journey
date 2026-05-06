# Practice: Python to C++ or Rust with an LLM

This folder contains a small beginner practice project.

The script [translate.py](translate.py) reads Python code and asks an LLM to translate it into C++ or Rust.

An **LLM** is a large language model. An **API** is a way for this script to send a request to an external model service and receive a response.

This project is not a compiler. Always review, compile, and test the output.

## Files in this folder

- [translate.py](translate.py): The Python script that calls the model API.
- [prompts.md](prompts.md): The system and user prompt templates, explained line by line.
- [code-walkthrough.md](code-walkthrough.md): The Python script explained line by line.

## Setup terms

Before running the script, know these words:

- **Package:** Code someone else wrote that you can install and use.
- **SDK:** A package made to help your code use a service. The OpenAI and Anthropic packages are SDKs.
- **Environment variable:** A named value stored outside your code. It is useful for secrets like API keys.
- **API key:** A secret string that proves your account is allowed to use an API.
- **Provider:** The company or service that runs the model. This script supports OpenAI and Anthropic.

## Install packages

Run this from the `code-translation` folder or from your project environment:

```bash
pip install openai
pip install anthropic
```

Line by line:

| Line | Meaning |
| --- | --- |
| `pip install openai` | Installs the OpenAI Python SDK. You need this if `LLM_PROVIDER` is `openai`. |
| `pip install anthropic` | Installs the Anthropic Python SDK. You need this if `LLM_PROVIDER` is `anthropic`. |

You only need the package for the provider you plan to use. Installing both is fine for practice.

## Set API keys

Use one or both of these commands:

```bash
export OPENAI_API_KEY="your_openai_key_here"
export ANTHROPIC_API_KEY="your_anthropic_key_here"
```

Line by line:

| Line | Meaning |
| --- | --- |
| `export OPENAI_API_KEY="your_openai_key_here"` | Creates an environment variable named `OPENAI_API_KEY`. The OpenAI SDK reads it when the script calls OpenAI. Replace the placeholder with your real key. |
| `export ANTHROPIC_API_KEY="your_anthropic_key_here"` | Creates an environment variable named `ANTHROPIC_API_KEY`. The Anthropic SDK reads it when the script calls Anthropic. Replace the placeholder with your real key. |

Do not commit real API keys to git.

## Choose provider and model

These settings are optional:

```bash
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o-mini"
```

Line by line:

| Line | Meaning |
| --- | --- |
| `export LLM_PROVIDER="openai"` | Tells the script which provider to use. Valid values are `openai` and `anthropic`. If you skip this, the script uses `openai`. |
| `export LLM_MODEL="gpt-4o-mini"` | Tells the script which model name to send to the provider. If you skip this, the script uses `gpt-4o-mini`. |

If you use Anthropic, choose a model name that your Anthropic account can access.

## Run from a file

Use this command when your Python code is saved in a file:

```bash
python translate.py --target cpp --file your_script.py
```

Line by line:

| Part | Meaning |
| --- | --- |
| `python` | Starts Python. |
| `translate.py` | Runs this practice script. |
| `--target cpp` | Tells the script to ask for C++ output. Use `--target rust` for Rust. |
| `--file your_script.py` | Tells the script which Python file to read. Replace `your_script.py` with your file path. |

## Run from standard input

Use this command when you want to pipe code into the script:

```bash
cat your_script.py | python translate.py --target rust
```

Line by line:

| Part | Meaning |
| --- | --- |
| `cat your_script.py` | Prints the contents of `your_script.py`. |
| `|` | Sends the printed text into the next command. This is called a pipe. |
| `python translate.py --target rust` | Runs the script and asks for Rust output. Because no `--file` is given, the script reads from standard input. |

## Add an extra note

Use `--note` when you want to add one more instruction:

```bash
python translate.py --target cpp --file your_script.py --note "Use only the C++ standard library."
```

Line by line:

| Part | Meaning |
| --- | --- |
| `python translate.py` | Runs the practice script. |
| `--target cpp` | Asks for C++ output. |
| `--file your_script.py` | Reads Python code from `your_script.py`. |
| `--note "Use only the C++ standard library."` | Adds an extra instruction to the user prompt. The quotes keep the sentence together as one value. |

## What happens when you run it

The script prints:

- The provider.
- The model name.
- The target language.
- The translated code returned by the model.

If something fails, the script prints an error message and exits.

## Safety checklist

- Do not paste private code into an external API unless your policy allows it.
- Start with small files.
- Compile the translated C++ or Rust.
- Run tests against the original Python behavior.
- Review the output before using it.
