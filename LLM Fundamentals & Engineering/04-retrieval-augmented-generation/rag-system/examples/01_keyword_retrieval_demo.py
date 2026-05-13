"""
Day 1 style demo: no vectors — load Markdown into memory and pick context by
simple keyword overlap (teaches why smarter retrieval is needed later).

Run from anywhere::

    python examples/01_keyword_retrieval_demo.py
"""

from __future__ import annotations

import glob
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent


def load_employee_knowledge() -> dict[str, str]:
    knowledge: dict[str, str] = {}
    for filename in glob.glob(str(ROOT / "knowledge-base" / "employees" / "*.md")):
        stem = Path(filename).stem
        last = stem.split()[-1]
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[last.lower()] = f.read()
    return knowledge


def load_product_knowledge() -> dict[str, str]:
    knowledge: dict[str, str] = {}
    for filename in glob.glob(str(ROOT / "knowledge-base" / "products" / "*.md")):
        stem = Path(filename).stem.lower()
        with open(filename, "r", encoding="utf-8") as f:
            knowledge[stem] = f.read()
    return knowledge


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def get_relevant_context(question: str, knowledge: dict[str, str]) -> str:
    q_tokens = tokenize(question)
    best_key = None
    best_score = 0
    for key, doc in knowledge.items():
        doc_tokens = tokenize(doc)
        score = len(q_tokens & doc_tokens)
        if score > best_score:
            best_score = score
            best_key = key
    if best_key is None or best_score == 0:
        return ""
    return f"[Matched bucket: {best_key} | overlap score: {best_score}]\n\n{knowledge[best_key][:2000]}"


def main():
    load_dotenv(override=True)
    model = os.environ.get("INSURELLM_DEMO_MODEL", "gpt-4.1-nano")
    client = OpenAI()

    employees = load_employee_knowledge()
    products = load_product_knowledge()
    merged = {**employees, **products}

    question = "Who won the IIOTY award in 2023?"
    print("Question:", question)
    context = get_relevant_context(question, merged)
    print("\n--- Retrieved context (keyword overlap) ---\n")
    print(context[:1200] if context else "(no context matched)")
    print("\n--- ... (truncated if long) ---\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the context if it helps; if context is empty or irrelevant, say you are not sure.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    reply = response.choices[0].message.content
    print("Model answer:\n", reply)


if __name__ == "__main__":
    main()
