# Practice: Code Translation Prompts and Project

## Goal

This guide prepares you for the optional code practice in [../code-translation/readme.md](../code-translation/readme.md).

The practice asks an LLM to translate Python code into C++ or Rust.

**Translate** means "rewrite the same idea in another language." Here, the input is Python source code. The output is C++ or Rust source code.

## Important warning

An LLM is not a compiler.

A **compiler** is a program that checks and turns source code into something the computer can run. C++ and Rust usually use compilers.

An LLM can create a useful first draft, but it can still:

- Miss edge cases.
- Invent a library function.
- Change behavior by accident.
- Use the wrong type.
- Return code that does not compile.

Always compile, test, and review translated code.

## What the practice script does

The script is [../code-translation/translate.py](../code-translation/translate.py).

It does this:

1. Reads Python code from a file or from standard input.
2. Builds a user message that includes the Python code.
3. Chooses a system prompt for C++ or Rust.
4. Sends both messages to an LLM API.
5. Prints the model's translated code.

**Standard input**, often called `stdin`, means text that is passed into a program instead of read from a named file.

An **API** is a way for one program to talk to another program or service.

## What a system prompt is

A **system prompt** is the instruction that sets the model's role and rules.

In this project, the system prompt says things like:

- Translate Python to C++ or Rust.
- Preserve behavior when possible.
- Use standard libraries unless the user allows more.
- Return only code in a fenced code block.

A **fenced code block** is Markdown text surrounded by triple backticks. It helps readers and tools identify code.

The full prompt templates are explained line by line in [../code-translation/prompts.md](../code-translation/prompts.md).

## What a user prompt is

A **user prompt** is the request for this specific run.

In this project, the user prompt includes:

- The target language.
- The Python source code.
- Extra notes from the command line, if you pass any.

The system prompt gives stable rules. The user prompt gives the actual task.

## How to evaluate the output

Use small programs first.

Good first examples:

- A function that adds numbers.
- A loop that counts items.
- A script that reads a small text file.
- A function that uses a list or dictionary.

Then check the result:

- Compile the C++ or Rust.
- Run the original Python and translated code with the same inputs.
- Compare outputs.
- Look for off-by-one errors.
- Check integer division, string handling, and file paths.

## Where to go next

Read these files in order:

1. [../code-translation/readme.md](../code-translation/readme.md) for setup and run commands.
2. [../code-translation/prompts.md](../code-translation/prompts.md) for line-by-line prompt explanations.
3. [../code-translation/code-walkthrough.md](../code-translation/code-walkthrough.md) for line-by-line Python code explanations.

You have finished the numbered guides in module 03.
