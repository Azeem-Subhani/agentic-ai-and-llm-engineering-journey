# 02 — Embeddings and vector databases

## What this guide is about

You will learn what an **embedding** is without linear algebra prerequisites, why **vector databases** exist, and how this module stores chunks in **Chroma**.

## What is an embedding?

An **embedding** is a **list of numbers** (a **vector**) produced by a model that was trained so that:

- similar sentences end up with **similar** vectors,
- unrelated sentences end up **far apart**.

Think of it as turning text into GPS coordinates in a high-dimensional space: “close” means “similar meaning,” not “similar spelling.”

### Inspect one embedding (OpenAI)

After you configure `OPENAI_API_KEY`, you can print the first few dimensions:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
resp = client.embeddings.create(model="text-embedding-3-large", input="Insurellm sells insurance software.")
vec = resp.data[0].embedding
print("dimensions:", len(vec))
print("first 8 values:", [round(x, 5) for x in vec[:8]])
```

**Example output:**

```text
dimensions: 3072
first 8 values: [-0.02137, 0.01452, -0.00391, 0.00814, -0.01022, 0.00456, -0.00188, 0.01290]
```

What this output tells you: one short sentence became **3072** floats — that is the shape of `text-embedding-3-large` in this project.

## Why similar text “clusters”

If you embed two phrases:

```python
from openai import OpenAI
from dotenv import load_dotenv
import math

load_dotenv()
client = OpenAI()
model = "text-embedding-3-large"

def emb(text: str):
    return client.embeddings.create(model=model, input=text).data[0].embedding

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)

t1 = "car insurance pricing"
t2 = "automobile policy premiums"
t3 = "chocolate cake recipe"
v1, v2, v3 = emb(t1), emb(t2), emb(t3)
print("sim(t1,t2) =", round(cosine_sim(v1, v2), 4))
print("sim(t1,t3) =", round(cosine_sim(v1, v3), 4))
```

**Example output:**

```text
sim(t1,t2) = 0.8421
sim(t1,t3) = 0.1124
```

What this output tells you: **paraphrases** about the same topic score higher than a random unrelated sentence — that is the property retrieval relies on.

## What a vector database does

Once every chunk has a vector, a **vector database**:

1. stores `(chunk_text, vector, metadata)` tuples,
2. answers queries like “give me the **k** chunks whose vectors are closest to this question vector.”

Analogy: a library sorted not alphabetically, but by **meaning** — “books near this question.”

## Why Chroma here

**Chroma** is an embedded vector store with a simple Python API and a **persistent directory** (`vector_db/` or `preprocessed_db/`). It is enough for learning and many prototypes. In production you might choose managed services (Pinecone, Weaviate, pgvector, etc.) — tradeoffs appear in guide 10.

## Baseline ingest creates vectors (LangChain + Chroma)

From `rag-system/`:

```bash
python -m implementation.ingest
```

**Example output:**

```text
Loaded 76 source documents
Created 432 chunks (size=500, overlap=200)
There are 432 vectors with 3,072 dimensions in the vector store
Ingestion complete
```

What this output tells you: every chunk is embedded with **`text-embedding-3-large`** (3072-D) and stored in Chroma under `rag-system/vector_db/`.

## Optional: local embeddings + t-SNE demo

[`rag-system/examples/02_embeddings_and_visualization.py`](../rag-system/examples/02_embeddings_and_visualization.py) uses **`sentence-transformers/all-MiniLM-L6-v2`** (smaller, runs locally) and can save a 2D scatter plot.

```bash
cd rag-system
python examples/02_embeddings_and_visualization.py
```

**Example output:**

```text
Loading Markdown from: .../rag-system/knowledge-base
Loaded 76 raw documents
Split into 210 chunks (size=1000, overlap=200)
Embedding model: sentence-transformers/all-MiniLM-L6-v2
Each chunk vector has dimension 384
First 8 values of one vector: [0.0312, -0.1204, 0.0088, ...]
Saved t-SNE plot to: .../rag-system/examples/_tsne_demo.png
```

What this output tells you: a **smaller** embedding model trades some quality for **speed and cost** — a common engineering decision.

## What to remember

- An **embedding** is a numeric fingerprint of meaning.
- A **vector database** finds the nearest neighbors in that space.
- This module’s **baseline** embeddings are OpenAI **`text-embedding-3-large`**; demos may use MiniLM locally.

Next: [`03-chunking-strategies.md`](03-chunking-strategies.md)
