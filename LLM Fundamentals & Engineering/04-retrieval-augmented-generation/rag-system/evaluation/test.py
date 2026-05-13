"""
Load the JSONL evaluation suite shipped with this module.

Each line is a ``TestQuestion`` used for retrieval metrics (keywords) and
answer judging (reference text).
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field


class TestQuestion(BaseModel):
    """One evaluation row: question, keyword probes, reference answer, category."""

    question: str = Field(description="The question to ask the RAG system")
    keywords: list[str] = Field(description="Keywords that must appear in retrieved context")
    reference_answer: str = Field(description="The reference answer for this question")
    category: str = Field(
        description="Question category (e.g., direct_fact, spanning, temporal)"
    )


def load_tests(filename: str | None = None) -> list[TestQuestion]:
    """
    Load tests from ``evaluation/<filename>`` (default: ``tests.jsonl``).

    Args:
        filename: Optional file name relative to this package directory.
    """
    path = Path(__file__).parent / (filename or "tests.jsonl")
    tests: list[TestQuestion] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            tests.append(TestQuestion(**data))
    return tests
