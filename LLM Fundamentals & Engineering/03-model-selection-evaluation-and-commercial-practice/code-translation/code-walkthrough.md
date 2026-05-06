# `translate.py` Code Walkthrough

This file explains [translate.py](translate.py) line by line.

The script has no custom classes. It uses functions and SDK classes from installed packages.

**Function** means a named block of code that does one job.

**Parameter** means an input value passed into a function.

**Method** means a function that belongs to an object.

**Class** means a blueprint for making objects. For example, `OpenAI` is a class from the OpenAI SDK.

## File header

```python
"""
Module 03 practice: translate Python source to C++ or Rust through an API.

Run (from this folder):
  python translate.py --target cpp --file sample.py
  cat sample.py | python translate.py --target rust

Requires API keys in the environment (see readme.md).
"""
```

Line by line:

| Line | Meaning |
| --- | --- |
| `"""` | Starts a multi-line string. At the top of a file, this is called a module docstring. It describes the file. |
| `Module 03 practice: translate Python source to C++ or Rust through an API.` | Says the script translates Python source code to C++ or Rust by calling an API. |
| Blank line | Separates the description from the run examples. |
| `Run (from this folder):` | Tells you the next lines are example commands. |
| `python translate.py --target cpp --file sample.py` | Example command that reads `sample.py` and asks for C++ output. |
| `cat sample.py \| python translate.py --target rust` | Example command that pipes `sample.py` into the script and asks for Rust output. |
| Blank line | Separates examples from requirements. |
| `Requires API keys...` | Reminds you that the script needs API keys stored in environment variables. |
| `"""` | Ends the multi-line string. |

## Imports

```python
from __future__ import annotations

import argparse
import os
import sys
from typing import List
```

Line by line:

| Line | Meaning |
| --- | --- |
| `from __future__ import annotations` | Makes Python handle type hints in a more flexible way. This helps with hints like `str \| None`. |
| Blank line | Separates future settings from normal imports. |
| `import argparse` | Imports Python's command-line argument parser. The script uses it to read `--target`, `--file`, and `--note`. |
| `import os` | Imports tools for reading environment variables. |
| `import sys` | Imports tools for standard input, standard error, and exiting. |
| `from typing import List` | Imports the `List` type hint. The script uses it for a list of strings. |

## Default settings

```python
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"
```

Line by line:

| Line | Meaning |
| --- | --- |
| `DEFAULT_PROVIDER = "openai"` | Sets the provider to OpenAI when the user does not choose one. |
| `DEFAULT_MODEL = "gpt-4o-mini"` | Sets the default model name when the user does not choose one. |

## Reading environment variables

An **environment variable** is a named value stored outside the code.

```python
_provider_raw = os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
PROVIDER = _provider_raw if _provider_raw in ("openai", "anthropic") else DEFAULT_PROVIDER
MODEL = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
```

Line by line:

| Line | Meaning |
| --- | --- |
| `_provider_raw = ...` | Reads `LLM_PROVIDER` from the environment. If it does not exist, it uses `DEFAULT_PROVIDER`. |
| `os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER)` | Looks up `LLM_PROVIDER`. The second value is the fallback. |
| `.lower()` | Converts the provider text to lowercase, so `OpenAI` and `openai` are treated the same. |
| `PROVIDER = ...` | Stores the provider the script will actually use. |
| `_provider_raw if _provider_raw in ("openai", "anthropic") else DEFAULT_PROVIDER` | Uses the chosen provider only if it is `openai` or `anthropic`. Otherwise, it falls back to OpenAI. |
| `MODEL = os.environ.get("LLM_MODEL", DEFAULT_MODEL)` | Reads `LLM_MODEL` from the environment. If it does not exist, it uses the default model name. |

## System prompt variables

The script has two long text variables:

- `SYSTEM_CPP`
- `SYSTEM_RUST`

These variables store the system prompts. A system prompt gives stable rules to the LLM.

The full text is explained in [prompts.md](prompts.md).

## `_read_source`

This function reads Python source code.

```python
def _read_source(path: str | None) -> str:
    if path:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `path` | The file path to read. It can be a string or `None`. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | The Python source code as text. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def _read_source(path: str \| None) -> str:` | Defines a function named `_read_source`. It accepts `path` and returns a string. |
| `if path:` | Checks if a file path was provided. |
| `with open(path, encoding="utf-8") as handle:` | Opens the file using UTF-8 text encoding. `with` closes the file automatically. |
| `return handle.read()` | Reads the whole file and returns it as text. |
| `return sys.stdin.read()` | If no file path was given, reads all text from standard input instead. |

## `_build_user_message`

This function creates the user prompt sent to the model.

```python
def _build_user_message(python_source: str, target: str, extra_note: str | None) -> str:
    label = "C++" if target == "cpp" else "Rust"
    note = (extra_note or "").strip()
    note_block = f"\n\nAdditional notes from the user:\n{note}\n" if note else ""
    return (
        f"Translate the following Python source to {label}.\n\n"
        "Constraints:\n"
        "- Preserve behavior; note any assumptions in comments in the output.\n"
        "- No third-party dependencies unless required by the source and supported in the target.\n\n"
        "Source:\n\n"
        f"{python_source.rstrip()}\n"
        f"{note_block}"
    )
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `python_source` | The Python code to translate. |
| `target` | The target language key. It should be `cpp` or `rust`. |
| `extra_note` | Optional extra instruction from `--note`. It can be text or `None`. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | A complete user message for the LLM. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def _build_user_message(...):` | Defines a function that builds the user prompt. |
| `label = "C++" if target == "cpp" else "Rust"` | Chooses the display name for the target language. |
| `note = (extra_note or "").strip()` | Uses an empty string if no note was given, then removes extra spaces at the start and end. |
| `note_block = ... if note else ""` | Builds the optional note section only when a note exists. Otherwise, it uses an empty string. |
| `return (` | Starts returning one combined string. Parentheses let the string span several lines. |
| `f"Translate... {label}.\n\n"` | Adds the main request. `{label}` becomes `C++` or `Rust`. `\n` means a new line. |
| `"Constraints:\n"` | Adds a heading for constraints. |
| `"- Preserve behavior...` | Tells the model to keep behavior the same and write assumptions as comments. |
| `"- No third-party dependencies...` | Tells the model not to add outside packages unless needed and supported. |
| `"Source:\n\n"` | Starts the source code section. |
| `f"{python_source.rstrip()}\n"` | Adds the Python source after removing extra whitespace from the end. |
| `f"{note_block}"` | Adds the optional note section. It may be empty. |
| `)` | Ends the returned string. |

## `_openai_chat`

This function sends the prompt to the OpenAI SDK.

```python
def _openai_chat(system: str, user: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (response.choices[0].message.content or "").strip()
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `system` | The system prompt with stable rules. |
| `user` | The user prompt with the source code and target language. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | The text answer from the model. |

Important class and method:

| Name | Meaning |
| --- | --- |
| `OpenAI` | A class from the OpenAI SDK. It creates a client object. |
| `client.chat.completions.create(...)` | A method call that sends a chat-style request to the model. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def _openai_chat(system: str, user: str) -> str:` | Defines a function that returns text from OpenAI. |
| `from openai import OpenAI` | Imports the OpenAI client class only when this function runs. |
| Blank line | Separates the import from the logic. |
| `client = OpenAI()` | Creates a client object. The SDK reads `OPENAI_API_KEY` from the environment. |
| `response = client.chat.completions.create(` | Sends a chat completion request and stores the response. |
| `model=MODEL,` | Sends the chosen model name. |
| `messages=[` | Starts the list of messages for the model. |
| `{"role": "system", "content": system},` | Sends the system prompt as a system message. |
| `{"role": "user", "content": user},` | Sends the user prompt as a user message. |
| `],` | Ends the message list. |
| `)` | Ends the API method call. |
| `return (response.choices[0].message.content or "").strip()` | Gets the first answer, uses an empty string if no content exists, removes extra edge spaces, and returns it. |

## `_anthropic_text_blocks`

This helper function extracts text from an Anthropic response.

```python
def _anthropic_text_blocks(content: object) -> str:
    parts: List[str] = []
    for block in content:  # type: ignore[assignment]
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(p for p in parts if p).strip()
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `content` | The response content object returned by the Anthropic SDK. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | All text blocks joined into one string. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def _anthropic_text_blocks(content: object) -> str:` | Defines a function that extracts text from Anthropic content. |
| `parts: List[str] = []` | Creates an empty list of strings. Each text block will be added here. |
| `for block in content:` | Loops through each block in the response content. |
| `# type: ignore[assignment]` | Tells the type checker not to complain about this loop. It does not affect runtime behavior. |
| `if getattr(block, "type", None) == "text":` | Checks whether the block is a text block. `getattr` safely reads an attribute. |
| `parts.append(getattr(block, "text", "") or "")` | Reads the block text and adds it to the list. If text is missing, it adds an empty string. |
| `return "\n".join(p for p in parts if p).strip()` | Joins non-empty text parts with new lines, removes extra edge spaces, and returns the result. |

## `_anthropic_chat`

This function sends the prompt to the Anthropic SDK.

```python
def _anthropic_chat(system: str, user: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return _anthropic_text_blocks(response.content) or "(No text content returned by the model.)"
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `system` | The system prompt with stable rules. |
| `user` | The user prompt with the source code and target language. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | The text answer from the model, or a fallback message if no text is returned. |

Important class and method:

| Name | Meaning |
| --- | --- |
| `anthropic.Anthropic` | A class from the Anthropic SDK. It creates a client object. |
| `client.messages.create(...)` | A method call that sends a message request to the model. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def _anthropic_chat(system: str, user: str) -> str:` | Defines a function that returns text from Anthropic. |
| `import anthropic` | Imports the Anthropic SDK only when this function runs. |
| Blank line | Separates the import from the logic. |
| `client = anthropic.Anthropic()` | Creates a client object. The SDK reads `ANTHROPIC_API_KEY` from the environment. |
| `response = client.messages.create(` | Sends a message request and stores the response. |
| `model=MODEL,` | Sends the chosen model name. |
| `max_tokens=4096,` | Limits how many output tokens the model can return. |
| `system=system,` | Sends the system prompt. |
| `messages=[{"role": "user", "content": user}],` | Sends the user prompt as the only user message. |
| `)` | Ends the API method call. |
| `return _anthropic_text_blocks(...) or ...` | Extracts text from the response. If no text exists, returns a clear fallback message. |

## `translate`

This function chooses the correct provider and returns the translated code.

```python
def translate(python_source: str, target: str, extra_note: str | None = None) -> str:
    system = SYSTEM_CPP if target == "cpp" else SYSTEM_RUST
    user = _build_user_message(python_source, target, extra_note)
    if PROVIDER == "openai":
        return _openai_chat(system, user)
    if PROVIDER == "anthropic":
        return _anthropic_chat(system, user)
    raise ValueError(f"Unsupported LLM_PROVIDER: {PROVIDER!r}")
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `python_source` | The Python code to translate. |
| `target` | The target language key: `cpp` or `rust`. |
| `extra_note` | Optional extra instruction. It defaults to `None`. |

Return value:

| Return | Meaning |
| --- | --- |
| `str` | The translated code text returned by the model. |

Line by line:

| Line | Meaning |
| --- | --- |
| `def translate(...):` | Defines the main translation function. |
| `system = SYSTEM_CPP if target == "cpp" else SYSTEM_RUST` | Chooses the C++ system prompt for `cpp`; otherwise chooses the Rust prompt. |
| `user = _build_user_message(...)` | Builds the user prompt from the source code, target, and optional note. |
| `if PROVIDER == "openai":` | Checks whether the selected provider is OpenAI. |
| `return _openai_chat(system, user)` | Sends the prompts to OpenAI and returns the answer. |
| `if PROVIDER == "anthropic":` | Checks whether the selected provider is Anthropic. |
| `return _anthropic_chat(system, user)` | Sends the prompts to Anthropic and returns the answer. |
| `raise ValueError(...)` | Raises an error if the provider is not supported. This should be rare because earlier code already checks the provider. |

## `main`

This function handles the command-line interface.

A **command-line interface**, or **CLI**, is a way to run a program by typing commands in a terminal.

```python
def main() -> None:
    parser = argparse.ArgumentParser(description="Translate Python to C++ or Rust via an LLM API.")
    parser.add_argument(
        "--target",
        choices=("cpp", "rust"),
        required=True,
        help="Output language family (C++ or Rust).",
    )
```

Line by line:

| Line | Meaning |
| --- | --- |
| `def main() -> None:` | Defines the main function. `None` means it does not return a useful value. |
| `parser = argparse.ArgumentParser(...)` | Creates an argument parser object. It reads command-line options. |
| `description="..."` | Sets help text for the whole script. |
| `parser.add_argument(` | Starts adding a command-line option. |
| `"--target",` | Names the option. The user writes `--target cpp` or `--target rust`. |
| `choices=("cpp", "rust"),` | Allows only `cpp` or `rust`. |
| `required=True,` | Makes this option required. |
| `help="...",` | Sets help text for this option. |
| `)` | Ends the `add_argument` call. |

```python
    parser.add_argument(
        "--file",
        "-f",
        help="Path to a .py file. If omitted, read Python source from stdin.",
    )
    parser.add_argument(
        "--note",
        "-n",
        help="Optional extra instructions appended to the user message.",
    )
```

Line by line:

| Line | Meaning |
| --- | --- |
| `parser.add_argument(` | Starts defining another command-line option. |
| `"--file",` | Adds the long option name. The user can write `--file your_script.py`. |
| `"-f",` | Adds a short option name. The user can write `-f your_script.py`. |
| `help="Path to a .py file..."` | Explains that the file is optional. Without it, the script reads from standard input. |
| `)` | Ends the file option setup. |
| `parser.add_argument(` | Starts defining the note option. |
| `"--note",` | Adds the long note option. |
| `"-n",` | Adds the short note option. |
| `help="Optional extra instructions..."` | Explains what the note does. |
| `)` | Ends the note option setup. |

```python
    args = parser.parse_args()
```

Line by line:

| Line | Meaning |
| --- | --- |
| `args = parser.parse_args()` | Reads the command-line options and stores them on `args`. Examples are `args.target`, `args.file`, and `args.note`. |

```python
    try:
        source = _read_source(args.file)
    except OSError as exc:
        print("Error reading source:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
```

Line by line:

| Line | Meaning |
| --- | --- |
| `try:` | Starts code that may fail. |
| `source = _read_source(args.file)` | Reads Python source from the file path or from standard input. |
| `except OSError as exc:` | Catches file or input errors and stores the error as `exc`. |
| `print("Error reading source:", exc, file=sys.stderr)` | Prints the error to standard error, which is used for error messages. |
| `raise SystemExit(1) from exc` | Stops the script with exit code `1`, which means failure. |

```python
    if not source.strip():
        print("Error: no Python source provided (empty file or stdin).", file=sys.stderr)
        raise SystemExit(1)
```

Line by line:

| Line | Meaning |
| --- | --- |
| `if not source.strip():` | Checks whether the source is empty after removing spaces and new lines. |
| `print("Error: no Python source...", file=sys.stderr)` | Prints a clear error message to standard error. |
| `raise SystemExit(1)` | Stops the script with failure code `1`. |

```python
    print("Provider:", PROVIDER)
    print("Model:", MODEL)
    print("Target:", args.target)
    print()
```

Line by line:

| Line | Meaning |
| --- | --- |
| `print("Provider:", PROVIDER)` | Shows which provider will be used. |
| `print("Model:", MODEL)` | Shows which model name will be used. |
| `print("Target:", args.target)` | Shows whether the target is `cpp` or `rust`. |
| `print()` | Prints a blank line before the model output. |

```python
    try:
        out = translate(source, args.target, args.note)
    except Exception as exc:  # noqa: BLE001 — educational script
        print("Error:", exc, file=sys.stderr)
        raise SystemExit(1) from exc
```

Line by line:

| Line | Meaning |
| --- | --- |
| `try:` | Starts code that may fail while calling the API. |
| `out = translate(source, args.target, args.note)` | Calls the main translation function and stores the result. |
| `except Exception as exc:` | Catches any error from translation. |
| `# noqa: BLE001 ...` | Tells a linter not to warn about catching a broad exception. This is acceptable here because the script is educational. |
| `print("Error:", exc, file=sys.stderr)` | Prints the error to standard error. |
| `raise SystemExit(1) from exc` | Stops the script with failure code `1`. |

```python
    print(out)
```

Line by line:

| Line | Meaning |
| --- | --- |
| `print(out)` | Prints the translated code returned by the model. |

## Script entry point

```python
if __name__ == "__main__":
    main()
```

Line by line:

| Line | Meaning |
| --- | --- |
| `if __name__ == "__main__":` | Checks whether this file is being run directly, instead of imported by another file. |
| `main()` | Runs the command-line program. |

## Full flow

When you run the script:

1. Python loads imports and settings.
2. `main()` reads command-line options.
3. `_read_source()` reads your Python code.
4. `translate()` chooses the prompt and provider.
5. `_openai_chat()` or `_anthropic_chat()` calls the API.
6. The script prints the model output.

That is the whole program: read source, build prompts, call provider, print output.
