# Examples (progressive demos)

Run these from the **`rag-system/`** directory so imports resolve (`implementation`, `evaluation`, etc.).

| Script | Needs | Purpose |
|--------|-------|---------|
| `01_keyword_retrieval_demo.py` | `OPENAI_API_KEY` | Keyword-overlap “retrieval” + one chat completion. |
| `02_embeddings_and_visualization.py` | HF model download on first run | Chunk + embed; optional t-SNE PNG. |
| `03_basic_rag_demo.py` | Ingested `vector_db/` | One RAG question via `answer_question`. |
| `04_evaluation_demo.py` | Ingested `vector_db/` | Retrieval metrics for test row 0. |
| `05_advanced_rag_demo.py` | `preprocessed_db/` | Rewrite + dual retrieval + rerank demo. |

```bash
cd rag-system
python examples/03_basic_rag_demo.py
```

**Example output:**

```text
Question: How many employees does Insurellm currently have?
...
Answer:
 Insurellm currently has 32 employees.
```
