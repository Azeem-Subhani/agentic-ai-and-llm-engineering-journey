# Week 2 — Tool calling (flight agent demo)

This folder is a **hands-on lesson** for people learning how large language models can **call tools** (sometimes called *function calling*). You can read this file first with **no coding background**, then open [`tool_calling.py`](tool_calling.py) to see the same ideas in code.

---

## What is tool calling?

Usually you send a question and the model answers with **text only**.

With **tool calling**, the model can also say, in a structured way: **“Please run this named function with these arguments.”** Your Python program **runs** that function (for example, it reads a database or a file), gets a **real result**, and sends that result **back** to the model. The model then writes the **final answer** for the user using the real data.

Think of it as the model raising a hand: *“I need the schedule from the filing cabinet,”* and your code being the person who opens the cabinet and hands the paper back.

---

## Why is it useful?

- **Fresh or private data:** Models only know what they were trained on unless you give them new text. Tools let you inject **live** or **private** information (flights, inventory, your company wiki).
- **Accuracy:** If the answer must match a database, the model should **read** that database through a tool instead of guessing times and prices.
- **Actions (later):** The same pattern can connect to booking systems, calculators, or other APIs—still with human oversight where it matters.

---

## How this “flight agent” example works

1. You (or the script) ask a **user question**, for example about flights between two cities on a date.
2. A **system prompt** tells the model it is a **flight assistant** and that it **must** use the `search_flights` tool for flight facts—**not** invent schedules.
3. The model’s first reply might be a **tool request**: *run `search_flights` with origin, destination, and optional date*.
4. Your script runs **`search_flights`**, which reads **[`flights.json`](flights.json)** and returns matching rows as **JSON text**.
5. That JSON is sent back to the model as a **tool result**.
6. The model writes a **friendly, human-readable** summary (times, prices, options).

So the model does **two** useful steps here: decide *when* to look data up, and then *explain* the data clearly.

---

## How the data flows (big picture)

```text
User question
    →
LLM (sees question + tool definitions)
    →
If needed: “call search_flights(…)”
    →
Your code runs search_flights → reads flights.json
    →
Tool result (JSON) sent back to LLM
    →
LLM writes final natural-language answer
    →
You print or show that answer
```

This is the same pattern many production apps use—only the tools and data sources change.

---

## How [`tool_calling.py`](tool_calling.py) is structured

The file is written in **numbered sections** so you can jump between this readme and the code.

| Section | What it does |
|--------|----------------|
| **1) Configuration** | Chooses **provider** (OpenAI or Anthropic), **model name**, optional **verbosity**, and how many **tool rounds** are allowed before stopping. |
| **2) System prompt** | Defines the **flight agent** behavior: use tools for schedules, do not make up flights. |
| **3) Tool implementation** | **`search_flights`** loads [`flights.json`](flights.json) and filters by origin, destination, and optional date. **`run_search_flights_tool`** parses the model’s arguments and returns JSON text. |
| **4) OpenAI path** | **`_run_with_openai`**: Chat Completions loop—if the model returns `tool_calls`, the script appends **tool** messages with results and calls the API again until the model returns normal text. |
| **5) Anthropic path** | **`_run_with_anthropic`**: Messages API loop—if `stop_reason` is `tool_use`, the script sends **`tool_result`** blocks and calls the API again. |
| **6) Entry point** | **`main`** prints a built-in demo question and the final assistant reply. **`run_demo`** is the single entry if you import this file elsewhere. |

Open the file and search for those section headers (`# ---` lines).

---

## Provider and model selection

### Easiest way: edit the defaults in code

At the top of [`tool_calling.py`](tool_calling.py), set:

- `DEFAULT_PROVIDER` to `"openai"` or `"anthropic"`
- `DEFAULT_MODEL` to one of the model strings below

`LLM_PROVIDER` and `LLM_MODEL` **environment variables** override those defaults (handy for terminals or CI without editing files).

### Supported options (copy-paste)

Provider names are always **`openai`** or **`anthropic`**.

| Provider   | Model label (readme)   | Value to put in `DEFAULT_MODEL` / `LLM_MODEL` |
|-----------|-------------------------|-----------------------------------------------|
| OpenAI    | gpt-4o-mini             | `gpt-4o-mini` |
| OpenAI    | gpt-5o-mini             | `gpt-5o-mini` |
| Anthropic | claude-3.5-sonnet       | `claude-3-5-sonnet-20241022` |
| Anthropic | claude-3-haiku          | `claude-3-haiku-20240307` |

**Important:** vendors rename and retire models. If a call fails with “model not found,” check the latest **OpenAI** or **Anthropic** model list and swap in the current ID. The lesson is the same even if the exact string changes.

### API keys

- **OpenAI:** set `OPENAI_API_KEY` in your environment.
- **Anthropic:** set `ANTHROPIC_API_KEY` in your environment.

Never commit API keys to git. This repo’s [`.gitignore`](../../../.gitignore) already ignores typical secret files like `.env`.

---

## Install and run

```bash
cd "LLM Fundamentals & Engineering/foundations/tool-calling"
pip install openai anthropic
export OPENAI_API_KEY="your_key"           # if using OpenAI
# export ANTHROPIC_API_KEY="your_key"      # if using Anthropic
python tool_calling.py
```

Optional: print which tool round ran:

```bash
export TOOL_CALLING_VERBOSE=true
python tool_calling.py
```

---

## Files in this folder

| File | Role |
|------|------|
| [`readme.md`](readme.md) | This explanation (read first). |
| [`tool_calling.py`](tool_calling.py) | Runnable demo: chat + tool loop for OpenAI or Anthropic. |
| [`flights.json`](flights.json) | Small **fake** schedule used as the “database.” |

---

## Suggested learning path

1. Read **What is tool calling** and **Why is it useful** above.  
2. Skim **How the flight agent example works** and **How the data flows**.  
3. Open [`tool_calling.py`](tool_calling.py) from section **1** through **6**, matching this readme.  
4. Run the script once with **OpenAI**, then (if you have a key) with **Anthropic**, changing only `DEFAULT_PROVIDER` and `DEFAULT_MODEL`.  
5. Edit [`flights.json`](flights.json) and ask a question that matches your new rows—watch the tool return your changes.

You now have a minimal, realistic pattern you can reuse for other tools and data sources.
