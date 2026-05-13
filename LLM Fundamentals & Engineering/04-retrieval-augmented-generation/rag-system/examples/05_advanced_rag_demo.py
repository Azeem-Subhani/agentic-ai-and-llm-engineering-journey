"""
Day 5 style demo: advanced stack (rewrite + dual retrieval + rerank).

Requires ``preprocessed_db`` from ``python -m pro_implementation.ingest``.

Run::

    python examples/05_advanced_rag_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    db = ROOT / "preprocessed_db"
    if not db.exists():
        print("preprocessed_db not found. Run: python -m pro_implementation.ingest")
        sys.exit(1)

    from pro_implementation.answer import answer_question, fetch_context, rewrite_query

    q = "Who is responsible for brand strategy leadership?"
    print("Question:", q)
    rq = rewrite_query(q, history=[])
    print("Rewritten KB query:", rq)
    chunks = fetch_context(q)
    print(f"\nFetched {len(chunks)} reranked chunks. First source:")
    if chunks:
        print(" ", chunks[0].metadata.get("source"))
        print(" ", chunks[0].page_content[:300].replace("\n", " "), "...")

    ans, final_chunks = answer_question(q, history=[])
    print("\nAnswer:\n", ans)


if __name__ == "__main__":
    main()
