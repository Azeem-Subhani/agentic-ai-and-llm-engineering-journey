"""
Module 03 practice: translate Python source to C++ or Rust through an API.

Run (from this folder):
  python translate.py --target cpp --file sample.py
  cat sample.py | python translate.py --target rust

Requires API keys in the environment (see readme.md).
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

# ---------------------------------------------------------------------------
# 1) Configuration — match module 01 tool-calling style
# ---------------------------------------------------------------------------
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"

_provider_raw = os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
PROVIDER = _provider_raw if _provider_raw in ("openai", "anthropic") else DEFAULT_PROVIDER
MODEL = os.environ.get("LLM_MODEL", DEFAULT_MODEL)

# ---------------------------------------------------------------------------
# 2) System prompts — see prompts.md (same text, for course reading)
# ---------------------------------------------------------------------------
SYSTEM_CPP = """You translate Python to idiomatic C++.

Rules:
- Preserve behavior for the given code. If behavior cannot be guaranteed, state assumptions in comments at the top of the translation.
- Target: C++17 unless the user message specifies otherwise.
- Prefer the C++ standard library. Do not introduce external dependencies unless the user message allows it.
- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag cpp on the opening fence.
- Do not include conversational text outside the fenced block."""

SYSTEM_RUST = """You translate Python to idiomatic Rust.

Rules:
- Preserve behavior where possible; document any semantic gaps in comments at the top of the translation.
- Target: Rust 2021 edition unless the user message specifies otherwise.
- Use only the standard library unless the user message allows external crates.
- Output: return ONLY the translated source code in a single markdown fenced code block. Use the language tag rust on the opening fence.
- Do not include conversational text outside the fenced block."""


def _read_source(path: str | None) -> str:
    if path:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


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


def _anthropic_text_blocks(content: object) -> str:
    parts: List[str] = []
    for block in content:  # type: ignore[assignment]
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(p for p in parts if p).strip()


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


def translate(python_source: str, target: str, extra_note: str | None = None) -> str:
    system = SYSTEM_CPP if target == "cpp" else SYSTEM_RUST
    user = _build_user_message(python_source, target, extra_note)
    if PROVIDER == "openai":
        return _openai_chat(system, user)
    if PROVIDER == "anthropic":
        return _anthropic_chat(system, user)
    raise ValueError(f"Unsupported LLM_PROVIDER: {PROVIDER!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate Python to C++ or Rust via an LLM API.")
    parser.add_argument(
        "--target",
        choices=("cpp", "rust"),
        required=True,
        help="Output language family (C++ or Rust).",
    )
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
    args = parser.parse_args()

    try:
        source = _read_source(args.file)
    except OSError as exc:
        print("Error reading source:", exc, file=sys.stderr)
        raise SystemExit(1) from exc

    if not source.strip():
        print("Error: no Python source provided (empty file or stdin).", file=sys.stderr)
        raise SystemExit(1)

    print("Provider:", PROVIDER)
    print("Model:", MODEL)
    print("Target:", args.target)
    print()

    try:
        out = translate(source, args.target, args.note)
    except Exception as exc:  # noqa: BLE001 — educational script
        print("Error:", exc, file=sys.stderr)
        raise SystemExit(1) from exc

    print(out)


if __name__ == "__main__":
    main()
