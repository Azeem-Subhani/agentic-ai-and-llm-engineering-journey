# Prompt Templates for `translate.py`

This file explains the prompts used by [translate.py](translate.py).

A **prompt** is text sent to an LLM. The prompt tells the model what to do.

A **system prompt** sets stable rules. A **user prompt** gives the specific request for one run.

## C++ system prompt

This is the C++ system prompt used when you run `--target cpp`:

```text
You translate Python to idiomatic C++.

Rules:
- Preserve behavior for the given code. If behavior cannot be guaranteed, state assumptions in comments at the top of the translation.
- Target: C++17 unless the user message specifies otherwise.
- Prefer the C++ standard library. Do not introduce external dependencies unless the user message allows it.
- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag cpp on the opening fence.
- Do not include conversational text outside the fenced block.
```

Line by line:

| Line | Meaning |
| --- | --- |
| `You translate Python to idiomatic C++.` | Gives the model its role. "Idiomatic" means the output should look natural to C++ developers. |
| Blank line | Separates the role from the rules, so the prompt is easier to read. |
| `Rules:` | Starts the list of rules the model should follow. |
| `- Preserve behavior for the given code. If behavior cannot be guaranteed, state assumptions in comments at the top of the translation.` | Tells the model to keep the same behavior. If it cannot be exact, it should write assumptions as comments. |
| `- Target: C++17 unless the user message specifies otherwise.` | Sets the default C++ version. C++17 is a common modern version of C++. |
| `- Prefer the C++ standard library. Do not introduce external dependencies unless the user message allows it.` | Tells the model not to add outside packages unless the user allows them. |
| `- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag cpp on the opening fence.` | Makes the output predictable. It also tells the model to mark the code block as C++ for syntax highlighting. |
| `- Do not include conversational text outside the fenced block.` | Stops the model from adding extra explanation around the code. |

## Rust system prompt

This is the Rust system prompt used when you run `--target rust`:

```text
You translate Python to idiomatic Rust.

Rules:
- Preserve behavior where possible; document any semantic gaps in comments at the top of the translation.
- Target: Rust 2021 edition unless the user message specifies otherwise.
- Use only the standard library unless the user message allows external crates.
- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag rust on the opening fence.
- Do not include conversational text outside the fenced block.
```

Line by line:

| Line | Meaning |
| --- | --- |
| `You translate Python to idiomatic Rust.` | Gives the model its role. "Idiomatic" means the output should look natural to Rust developers. |
| Blank line | Separates the role from the rules. |
| `Rules:` | Starts the rule list. |
| `- Preserve behavior where possible; document any semantic gaps in comments at the top of the translation.` | Tells the model to keep behavior the same when it can. If Rust and Python behave differently, the model should write that gap as a comment. |
| `- Target: Rust 2021 edition unless the user message specifies otherwise.` | Sets the default Rust edition. An edition is a version group for Rust language rules. |
| `- Use only the standard library unless the user message allows external crates.` | Tells the model not to add outside Rust crates unless allowed. A crate is a Rust package. |
| `- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag rust on the opening fence.` | Makes the output easy to copy and test. It also tells the model to mark the code block as Rust for syntax highlighting. |
| `- Do not include conversational text outside the fenced block.` | Stops extra prose outside the code block. |

## User message shape

The script builds a user message like this:

```text
Translate the following Python source to {C++ or Rust}.

Constraints:
- Preserve behavior; note any assumptions in comments in the output.
- No third-party dependencies unless required by the source and supported in the target.

Source:

[PASTE YOUR PYTHON HERE]

Additional notes from the user:
[OPTIONAL NOTE]
```

Line by line:

| Line | Meaning |
| --- | --- |
| `Translate the following Python source to {C++ or Rust}.` | States the exact task and target language. The script replaces `{C++ or Rust}` with the real target. |
| Blank line | Separates the main request from the constraints. |
| `Constraints:` | Starts rules for this one request. |
| `- Preserve behavior; note any assumptions in comments in the output.` | Asks the model to keep the same behavior and write assumptions as comments. |
| `- No third-party dependencies unless required by the source and supported in the target.` | Avoids extra packages unless they are truly needed and supported. |
| Blank line | Separates constraints from the source section. |
| `Source:` | Starts the code input section. |
| Blank line | Keeps the source code visually separate. |
| `[PASTE YOUR PYTHON HERE]` | Placeholder for the Python code read from a file or standard input. |
| Blank line | Separates the source from optional notes. |
| `Additional notes from the user:` | Starts the optional note section when `--note` is used. |
| `[OPTIONAL NOTE]` | Placeholder for the text passed with `--note`. If no note is passed, this section is not included. |

## Why there are two prompt types

The system prompt stays stable. It describes the model's job and output rules.

The user prompt changes on each run. It contains your actual Python source code and any extra instruction.

This split keeps the program easier to control.
