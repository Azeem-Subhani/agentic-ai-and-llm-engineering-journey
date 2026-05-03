"""
Week 2 demo: tool calling with a flight agent.

Flow: user asks about flights -> model may request `search_flights` ->
your code runs the tool against `flights.json` -> results go back to the
model -> model writes a friendly final answer.

Run (from this folder):
    python tool_calling.py

Requires API keys in the environment (see readme.md).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# 1) Configuration — pick provider and model (env vars override for scripts/CI)
# ---------------------------------------------------------------------------
# Valid pairs (API model IDs change; confirm in provider docs if a call fails):
#   OpenAI:     "gpt-4o-mini", "gpt-5o-mini"
#   Anthropic:  "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"
#   (Friendly labels for Anthropic are listed in readme.md.)

DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini"

_provider_raw = os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
PROVIDER = _provider_raw if _provider_raw in ("openai", "anthropic") else DEFAULT_PROVIDER
MODEL = os.environ.get("LLM_MODEL", DEFAULT_MODEL)

MAX_TOOL_ROUNDS = 5
VERBOSE = os.environ.get("TOOL_CALLING_VERBOSE", "").lower() in ("1", "true", "yes")

DATA_PATH = Path(__file__).resolve().parent / "flights.json"

# ---------------------------------------------------------------------------
# 2) System prompt — flight agent must use tools for schedule lookups
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a helpful flight information assistant.

Rules:
- When the user asks about flights, routes, prices, or schedules, you MUST use
  the search_flights tool to look up data. Do not invent flights or prices.
- If the tool returns no rows, say clearly that no matching flights were found.
- After you receive tool results, summarize them in plain, friendly language."""

# ---------------------------------------------------------------------------
# 3) Tool implementation — reads local JSON (simulated flight database)
# ---------------------------------------------------------------------------


def _load_flights() -> List[Dict[str, Any]]:
    with DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def search_flights(
    origin: str,
    destination: str,
    date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Return flights matching origin and destination (case-insensitive).
    If `date` is provided (YYYY-MM-DD), filter to that date as well.
    """
    origin_key = origin.strip().lower()
    dest_key = destination.strip().lower()
    rows = _load_flights()
    matches: List[Dict[str, Any]] = []
    for flight in rows:
        if flight["origin"].lower() != origin_key:
            continue
        if flight["destination"].lower() != dest_key:
            continue
        if date and flight.get("date") != date.strip():
            continue
        matches.append(flight)
    return matches


def run_search_flights_tool(arguments: str | Dict[str, Any]) -> str:
    """Parse model-supplied arguments and return JSON text for the LLM."""
    payload: Dict[str, Any] = (
        arguments if isinstance(arguments, dict) else json.loads(arguments or "{}")
    )
    origin = str(payload.get("origin", "")).strip()
    destination = str(payload.get("destination", "")).strip()
    date = payload.get("date")
    date_str = str(date).strip() if date else None
    result = search_flights(origin, destination, date_str)
    return json.dumps(result, indent=2)


# JSON Schema shared conceptually by both providers
_TOOL_PARAMETERS: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "origin": {
            "type": "string",
            "description": "Departure city name, e.g. San Francisco",
        },
        "destination": {
            "type": "string",
            "description": "Arrival city name, e.g. Seattle",
        },
        "date": {
            "type": "string",
            "description": "Optional travel date in ISO format YYYY-MM-DD",
        },
    },
    "required": ["origin", "destination"],
}

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_flights",
            "description": (
                "Look up flights between two cities from the local schedule file. "
                "Use whenever the user asks about flights, prices, times, or routes."
            ),
            "parameters": _TOOL_PARAMETERS,
        },
    }
]

ANTHROPIC_TOOLS = [
    {
        "name": "search_flights",
        "description": (
            "Look up flights between two cities from the local schedule file. "
            "Use whenever the user asks about flights, prices, times, or routes."
        ),
        "input_schema": _TOOL_PARAMETERS,
    }
]


# ---------------------------------------------------------------------------
# 4) OpenAI — Chat Completions tool loop
# ---------------------------------------------------------------------------


def _run_with_openai(user_message: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for round_idx in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto",
        )
        choice = response.choices[0]
        message = choice.message

        if message.tool_calls:
            if VERBOSE:
                print(f"[openai] tool round {round_idx + 1}: {len(message.tool_calls)} call(s)")

            # Assistant turn that requests tools
            assistant_payload: Dict[str, Any] = {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            }
            messages.append(assistant_payload)

            for tc in message.tool_calls:
                if tc.function.name != "search_flights":
                    tool_text = json.dumps({"error": f"unknown tool: {tc.function.name}"})
                else:
                    tool_text = run_search_flights_tool(tc.function.arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_text,
                    }
                )
            continue

        # No tool calls — final natural language reply
        text = (message.content or "").strip()
        if text:
            return text
        return "(No text content returned by the model.)"

    return f"Stopped after {MAX_TOOL_ROUNDS} tool rounds without a final answer."


# ---------------------------------------------------------------------------
# 5) Anthropic — Messages API tool loop
# ---------------------------------------------------------------------------


def _extract_text_blocks(content: Any) -> str:
    parts: List[str] = []
    for block in content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(p for p in parts if p).strip()


def _anthropic_assistant_content_as_dicts(content: Any) -> List[Dict[str, Any]]:
    """Turn SDK content blocks into plain dicts for the next API request."""
    out: List[Dict[str, Any]] = []
    for block in content:
        btype = getattr(block, "type", None)
        if btype == "text":
            out.append({"type": "text", "text": getattr(block, "text", "") or ""})
        elif btype == "tool_use":
            out.append(
                {
                    "type": "tool_use",
                    "id": getattr(block, "id", ""),
                    "name": getattr(block, "name", ""),
                    "input": getattr(block, "input", {}) or {},
                }
            )
    return out


def _run_with_anthropic(user_message: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    messages: List[Dict[str, Any]] = [{"role": "user", "content": user_message}]

    for round_idx in range(MAX_TOOL_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=ANTHROPIC_TOOLS,
        )

        if response.stop_reason == "tool_use":
            if VERBOSE:
                print(f"[anthropic] tool round {round_idx + 1}")

            messages.append(
                {
                    "role": "assistant",
                    "content": _anthropic_assistant_content_as_dicts(response.content),
                }
            )

            tool_result_blocks: List[Dict[str, Any]] = []
            for block in response.content:
                if getattr(block, "type", None) != "tool_use":
                    continue
                tool_name = getattr(block, "name", "")
                tool_id = getattr(block, "id", "")
                raw_input = getattr(block, "input", {})
                if tool_name != "search_flights":
                    payload = json.dumps({"error": f"unknown tool: {tool_name}"})
                else:
                    payload = run_search_flights_tool(raw_input)
                tool_result_blocks.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": payload,
                    }
                )

            messages.append({"role": "user", "content": tool_result_blocks})
            continue

        # end_turn or max_tokens — return visible text
        text = _extract_text_blocks(response.content)
        if text:
            return text
        return "(No text content returned by the model.)"

    return f"Stopped after {MAX_TOOL_ROUNDS} tool rounds without a final answer."


# ---------------------------------------------------------------------------
# 6) Entry point
# ---------------------------------------------------------------------------


def run_demo(user_message: str) -> str:
    """Send one user turn through the configured provider and return assistant text."""
    if PROVIDER == "openai":
        return _run_with_openai(user_message)
    if PROVIDER == "anthropic":
        return _run_with_anthropic(user_message)
    raise ValueError(f"Unsupported PROVIDER: {PROVIDER!r}")


def main() -> None:
    demo_message = (
        "I need a morning-ish option: what flights go from San Francisco to Seattle "
        "on May 10, 2026? Please include times and prices."
    )

    print("Provider:", PROVIDER)
    print("Model:", MODEL)
    print("User:", demo_message)
    print()

    try:
        answer = run_demo(demo_message)
    except Exception as exc:  # noqa: BLE001 — educational script
        print("Error:", exc)
        return

    print("Assistant:")
    print(answer)


if __name__ == "__main__":
    main()
