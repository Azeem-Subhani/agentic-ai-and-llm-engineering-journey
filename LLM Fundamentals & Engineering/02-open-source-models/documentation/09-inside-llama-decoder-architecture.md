# Inside a Llama-Style Decoder Model

## How to use this guide

This document explains **one printed example** of a Hugging Face **`LlamaForCausalLM`** object—the tree that appeared in [`../notes.md`](../notes.md) and that you can also obtain by evaluating `model` in [`Week_3_Day_4_models.ipynb`](../Week_3_Day_4_models.ipynb) after loading Llama (cell 17).

**Important:** Exact numbers (**128256**, **4096**, **32 layers**, **1024** for K/V, etc.) depend on the **specific checkpoint** (8B vs smaller variants, grouped-query attention settings, etc.). Treat the tree below as a **pedagogical reference layout**; your printed lines may differ slightly, but the **names and roles** of blocks stay the same family-wide.

**Prerequisites:** [08-models-quantization-and-loading.md](08-models-quantization-and-loading.md), especially the idea of **token embeddings**, **decoder layers**, and **`lm_head`**.

---

## Part A — Decoder-only language models

**Llama** (in the configuration used in class) is a **decoder-only** transformer: it stacks identical **decoder blocks** one after another. There is **no separate encoder** (unlike original “encoder–decoder” translation transformers).

**Causal** means each position may attend only to **itself and previous positions** when computing attention—this preserves autoregressive “predict the next token” training.

---

## Part B — Why nonlinearity matters (short but precise)

Each block contains **linear** layers (matrix multiplications). If you composed only linear layers without breaks, the whole network would collapse mathematically into **one** giant linear map for many architectures—greatly limiting what patterns it could represent.

**Nonlinear activation functions** (here **`SiLU`**, also called **Swish**) introduce **curvature**: the model can approximate much richer input–output relationships. That is why you see `act_fn` inside the MLP block below—it is not decorative.

---

## Part C — Line-by-line on the printed tree

Below is the structure from class notes (slightly cleaned for typography). After each block: **what it is** and **what shape intuition to carry**.

```text
LlamaForCausalLM(
  (model): LlamaModel(
    (embed_tokens): Embedding(128256, 4096)
    (layers): ModuleList(
      (0-31): 32 x LlamaDecoderLayer(
        (self_attn): LlamaSdpaAttention(
          (q_proj): Linear(in_features=4096, out_features=4096, bias=False)
          (k_proj): Linear(in_features=4096, out_features=1024, bias=False)
          (v_proj): Linear(in_features=4096, out_features=1024, bias=False)
          (o_proj): Linear(in_features=4096, out_features=4096, bias=False)
          (rotary_emb): LlamaRotaryEmbedding()
        )
        (mlp): LlamaMLP(
          (gate_proj): Linear(in_features=4096, out_features=14336, bias=False)
          (up_proj): Linear(in_features=4096, out_features=14336, bias=False)
          (down_proj): Linear(in_features=14336, out_features=4096, bias=False)
          (act_fn): SiLU()
        )
        (input_layernorm): LlamaRMSNorm((4096,), eps=1e-05)
        (post_attention_layernorm): LlamaRMSNorm((4096,), eps=1e-05)
      )
    )
    (norm): LlamaRMSNorm((4096,), eps=1e-05)
  )
  (lm_head): Linear(in_features=4096, out_features=128256, bias=False)
)
```

### Top: `LlamaForCausalLM`

**What it is:** The **Python module** Hugging Face wraps around the inner `LlamaModel` plus the output projection used for **vocabulary logits** (scores per token).

---

### `LlamaModel` → `embed_tokens: Embedding(128256, 4096)`

**What it is:** A lookup table from **token ID** (row index) to a **4096-dimensional vector** of floats—the model’s internal notion of “what this token means” before any self-attention.

- **128256** — vocabulary size for this checkpoint (each possible token ID).  
- **4096** — **hidden size** (model width).

---

### `layers: ModuleList` with **32 × `LlamaDecoderLayer`**

**What it is:** The depth of the network. Each layer applies **attention** (mix information across positions) then **MLP** (position-wise processing), with normalization around those sub-blocks (see RMSNorm entries).

Your notes mention 32 layers; smaller Llama variants may use fewer—count the printed range `(0-N)`.

---

#### Inside one `LlamaDecoderLayer` — `self_attn: LlamaSdpaAttention`

**Self-attention** lets each token position gather information from allowed other positions (all previous tokens, for causal models).

**Projection lines:**

- **`q_proj: 4096 → 4096`** — maps hidden states to **query** vectors (full width here).  
- **`k_proj` and `v_proj: 4096 → 1024`** — **Key** and **value** projections to a **smaller width** than queries.

**Why are K and V smaller than Q here?**  
This pattern matches **grouped-query attention (GQA)** / **multi-query** style designs: many queries share fewer key/value heads to **save memory and speed** during autoregressive decoding. Exact ratios depend on architecture version; the **principle** is “not always identical Q/K/V dimensions.”

- **`o_proj: 4096 → 4096`** — **output projection** mixes attention head outputs back into the model’s hidden width.

- **`rotary_emb`** — **Rotary Position Embeddings (RoPE)** bake **position information** into Q and K without adding a separate big positional embedding table the way earliest transformers did.

---

#### `mlp: LlamaMLP` — the feed-forward block

Llama uses a **gated** feed-forward structure (often called **SwiGLU** in papers):

- **`gate_proj` and `up_proj`** — two different linear expansions from hidden size **4096** to an **inner** dimension **14336** (expansion ratio is a design choice).  
- **`act_fn: SiLU`** — nonlinearity applied in the gating pathway.  
- **`down_proj: 14336 → 4096`** — projects back to residual stream width so the block can add back into the main signal.

**Intuition:** MLP lets each token **privately** transform its vector after attention mixed information across tokens.

---

#### `input_layernorm` and `post_attention_layernorm` — `LlamaRMSNorm`

**RMSNorm** (Root Mean Square normalization) stabilizes magnitudes **without** the extra mean-centering step of classic LayerNorm. There is one norm before attention and one before the MLP—this matches the **Pre-LN** transformer pattern used in Llama.

---

### Final `norm: LlamaRMSNorm` on `LlamaModel`

One more normalization after the last decoder block, before logits.

---

### `lm_head: Linear(4096, 128256)`

**What it is:** The **unembedding** step: turn each position’s final **4096-D** hidden vector into **128256** scores—one score per vocabulary token—for **next-token prediction**.

**Bias False:** no per-output bias vector; common in many LLM heads.

**Tie-in:** In some implementations, weights can be **tied** (shared) with `embed_tokens` to save parameters; whether printing shows that depends on version. Conceptually, `embed_tokens` and `lm_head` are inverses across the hidden width.

---

## Part D — How this connects to Day 4 code

1. `tokenizer.apply_chat_template(...)` builds the **prompt token IDs**.  
2. `embed_tokens` converts those IDs to vectors.  
3. The **stack of decoder layers** updates those vectors.  
4. `lm_head` produces logits; **`generate`** applies sampling or greedy picking repeatedly.

When you print `model` in the notebook, you are seeing the **static architecture**. When you call `model.generate`, you are running **forward passes** through that graph.

---

## Part E — Recap checklist

You can now:

- Name the two big halves of each decoder layer (**attention** vs **MLP**) and why **SiLU** appears.  
- Explain **embeddings** vs **`lm_head`** as opposites across the hidden dimension.  
- Recognize **RoPE** and why K/V projections may be narrower than Q in some Llama variants.

---

## Next guide

[10-meeting-minutes-audio-product.md](10-meeting-minutes-audio-product.md) applies similar loading patterns to a **speech → text → report** pipeline.
