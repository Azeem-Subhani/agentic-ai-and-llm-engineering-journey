"""
Day 4 style demo: load one test row and print retrieval metrics (no judge call).

For full judge + answer scoring use ``python evaluation/eval.py <n>``.

Run::

    python examples/04_evaluation_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from evaluation.eval import evaluate_retrieval
from evaluation.test import load_tests

load_dotenv(override=True)


def main():
    tests = load_tests()
    print(f"Loaded {len(tests)} tests from tests.jsonl")
    t = tests[0]
    print("\nSample test row #0:")
    print("  question:", t.question)
    print("  keywords:", t.keywords)
    print("  category:", t.category)

    r = evaluate_retrieval(t)
    print("\nRetrieval metrics:")
    print(f"  MRR: {r.mrr:.4f}")
    print(f"  nDCG: {r.ndcg:.4f}")
    print(f"  keywords_found: {r.keywords_found}/{r.total_keywords}")
    print(f"  keyword_coverage: {r.keyword_coverage:.1f}%")


if __name__ == "__main__":
    main()
