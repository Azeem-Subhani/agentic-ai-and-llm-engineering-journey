"""
Day 3 style demo: call the same ``answer_question`` used by ``app.py``.

Requires an ingested ``vector_db`` (run ``python -m implementation.ingest`` first).

Run::

    python examples/03_basic_rag_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from implementation.answer import answer_question

load_dotenv(override=True)


def main():
    q = "How many employees does Insurellm currently have?"
    print("Question:", q)
    answer, docs = answer_question(q, history=[])
    print("\nTop sources:")
    for i, d in enumerate(docs[:3], 1):
        src = d.metadata.get("source", "?")
        preview = d.page_content[:200].replace("\n", " ")
        print(f"  {i}. {src}\n     {preview}...")
    print("\nAnswer:\n", answer)


if __name__ == "__main__":
    main()
