# LLM Fundamentals: A Simple Step-by-Step Course

Welcome. This page explains **large language models**, also called **LLMs**, from the very beginning.

You do not need a math background. You do not need a computer science background. We will build the ideas slowly, one step at a time.

In each section, we try to answer four small questions:

- **What is it?**
- **Why does it exist?**
- **How does it work?**
- **What is a simple real-life analogy?**

If a word is new, it will be explained before we use it.

---

## Table of contents

1. [Start here: what “model” and “LLM” mean](#1-start-here-what-model-and-llm-mean)
2. [Optional tools and file types you may see in a course](#2-optional-tools-and-file-types-you-may-see-in-a-course)
3. [The main types of language models](#3-the-main-types-of-language-models)
4. [Frontier models and reasoning budget](#4-frontier-models-and-reasoning-budget)
5. [Artificial neurons and neural networks](#5-artificial-neurons-and-neural-networks)
6. [What “parameters” means](#6-what-parameters-means)
7. [From characters to words to tokens](#7-from-characters-to-words-to-tokens)
8. [The transformer, explained clearly](#8-the-transformer-explained-clearly)
9. [LSTM and the short timeline of modern LLMs](#9-lstm-and-the-short-timeline-of-modern-llms)
10. [Prompt engineering, context engineering, RAG, and agentic AI](#10-prompt-engineering-context-engineering-rag-and-agentic-ai)
11. [Why an API call is stateless, but chat still feels like memory](#11-why-an-api-call-is-stateless-but-chat-still-feels-like-memory)
12. [Context window and cost](#12-context-window-and-cost)
13. [Python examples for calling OpenAI](#13-python-examples-for-calling-openai)
14. [Final recap](#14-final-recap)

---

## 1. Start here: what “model” and “LLM” mean

Before we talk about LLMs, we need two simple ideas.

### 1.1 What is a model?

**What it is:** A **model** is a computer system that learned patterns from many examples.

**Why it exists:** We want computers to do more than follow a fixed list of rules. We want them to learn from examples and make useful guesses in new situations.

**How it works:** During **training**, the model sees a lot of example data. **Training** means showing the model many examples and slowly adjusting its inside numbers so it gets better at its job.

**Analogy:** A model is like a student who did many practice questions. After enough practice, the student can answer a new question that looks similar.

### 1.2 What is a language model?

**What it is:** A **language model** is a model that works with language, which means words, sentences, and writing.

**Why it exists:** We want computers to read, write, summarize, explain, translate, and answer questions with human language.

**How it works:** It learns patterns in text, such as grammar, sentence structure, common facts, and the way ideas are usually written.

**Analogy:** It is like a reader who has seen a huge number of books and notices how sentences usually continue.

### 1.3 What is a large language model?

**What it is:** A **large language model**, or **LLM**, is a language model trained on a very large amount of text.

**Why it exists:** Bigger training often helps the model learn more language patterns and handle more kinds of tasks.

**How it works:** An LLM reads the text you give it and predicts what text should come next, one small piece at a time.

**Analogy:** Think of an LLM as a very powerful autocomplete system. It is much stronger than phone autocomplete, but the basic idea is similar: it keeps guessing the next piece of text.

### 1.4 One very important truth

An LLM is not a human brain.

- It does not think exactly like a person.
- It does not understand the world in the same deep way a person does.
- It can sound confident even when it is wrong.

Still, it can be very useful because it is very good at finding patterns in language and producing text that often sounds helpful.

**Quick recap:** A model learns from examples. A language model works with text. An LLM is a very large language model that predicts the next piece of text again and again.

---

## 2. Optional tools and file types you may see in a course

This section is optional. It explains some file types and tools from the course notes.

### 2.1 What is a `.md` file?

**What it is:** A `.md` file is a **Markdown** file.

**Why it exists:** Markdown lets people write clean notes with headings, lists, links, and code blocks without needing complicated software.

**How it works:** You type plain text and add simple symbols. For example, `#` makes a heading and `-` makes a bullet point.

**Analogy:** It is like writing a normal text note, but with a few easy marks that make it look neat.

### 2.2 What is a `.ipynb` file?

**What it is:** A `.ipynb` file is a **Jupyter Notebook** file.

**Why it exists:** It lets you mix explanation and code in one place, which is great for learning.

**How it works:** A notebook is split into **cells**. A **cell** is one small box. Some cells hold text. Some cells hold code. You can run the code one cell at a time.

**Analogy:** It is like a workbook where one box explains the idea and the next box lets you try it.

### 2.3 What is Ollama?

**What it is:** **Ollama** is a tool that can download and run some open models on your own computer.

**Why it exists:** It gives you a way to practice with local models instead of always using an online service.

**How it works:** You install it, start its local service, and run commands such as `ollama run gemma3:270m`.

**Analogy:** It is like keeping a small machine at home instead of borrowing one over the internet.

The course notes also mention:

- `ollama serve`
- `ollama run modelName:parameters`

These are common commands when working with Ollama.

### 2.4 What is `uv`?

**What it is:** `uv` is a tool that helps manage **Python** and Python project packages.

**Why it exists:** Python projects often need the right versions of the right tools. `uv` helps keep that clean and organized.

**How it works:** It can install Python, manage project packages, and sync the project setup.

Common commands from the notes:

- `uv --version`
- `uv self update`
- `uv sync`

**Analogy:** It is like a school bag organizer that makes sure you bring the right books for the class.

### 2.5 What is Cursor?

**What it is:** **Cursor** is a code editor. A **code editor** is a program used to read and write code files.

**Why it exists:** It helps you keep files, notes, and code in one place while learning.

**How it works:** You open a project folder and read or change files inside it.

The notes say to clone the **repository** and open it in Cursor. A **repository** is just a project folder that stores code and files, often with version history.

**Analogy:** Cursor is like a smart study desk for coding.

**Quick recap:** `.md` is a Markdown file. `.ipynb` is a notebook file. Ollama runs some models locally. `uv` helps with Python setup. Cursor is a code editor.

---

## 3. The main types of language models

Your notes mention three main kinds of LLMs, plus hybrid models.

### 3.1 Base models

**What it is:** A **base model** is the most basic form of a language model. Its main job is to continue text.

**Why it exists:** The next-step prediction task is simple and powerful. If a model gets very good at predicting what comes next, it learns a lot about language.

**How it works:** You give it some text, and it predicts the next word or next small piece of text. Then it does that again and again.

**Analogy:** It is like a super-strong version of phone autocomplete.

**Mini example:**

```text
Input:  "The sky is"
Output: "blue"
```

Then it can continue:

```text
"The sky is blue today."
```

By itself, a base model is not always a polished assistant. It is mainly good at continuing patterns.

### 3.2 Chat or instruct models

**What it is:** A **chat model** or **instruct model** is a model trained to respond like a helpful assistant.

**Why it exists:** People do not just want text continuation. They want the model to follow instructions, answer questions, and act more safely.

**How it works:** Teams take a strong base model and do extra training.

Two important training ideas are:

- **Instruction fine-tuning**: extra training on examples shaped like request -> good answer.
- **Reinforcement learning from human feedback (RLHF)**: people or rules score answers, and the model learns which answers are more helpful and safer.

Chat models often use message **roles**:

- **System**: high-level instructions, such as "be brief" or "act like a tutor"
- **User**: the person asking something
- **Assistant**: the model's reply

**Analogy:** A base model is like a student who can continue any paragraph. A chat model is like a student who was also taught how to answer a teacher politely and clearly.

### 3.3 Reasoning models

**What it is:** A **reasoning model** is a model trained to spend more effort on hard problems before giving the final answer.

**Why it exists:** Some tasks need more than a fast first guess. They need deeper step-by-step work.

**How it works:** The model uses more of its internal problem-solving process before answering.

**Analogy:** It is like a student who takes extra scratch paper before giving the final answer.

Two useful terms:

- **Reasoning budget**: how much thinking effort the model is allowed to use
- **Budget forcing**: ways to make a reasoning model spend more of that budget before answering

### 3.4 Hybrid models

**What it is:** A **hybrid model** mixes features from different styles of models.

**Why it exists:** People often want one model that can chat quickly but also think more deeply when needed.

**How it works:** The system is built or trained to support more than one behavior.

**Analogy:** It is like one person who can both answer quick questions and also sit down for careful homework help.

**Quick recap:** Base models continue text. Chat or instruct models are trained to answer like assistants. Reasoning models spend more effort on hard tasks. Hybrid models mix these strengths.

---

## 4. Frontier models and reasoning budget

### 4.1 What is a frontier model?

**What it is:** A **frontier model** is one of the strongest and newest models available from a major AI lab at a given time.

**Why it exists:** AI labs keep trying to build more capable models.

**How it works:** Labs train very large models with huge amounts of data and computer power.

**Analogy:** Frontier models are like the top students in a school at that moment. They are not perfect, but they are among the strongest.

Examples from your notes:

- **OpenAI** -> **GPT**
- **Anthropic** -> **Claude**
- **Google** -> **Gemini**
- **xAI** -> **Grok**
- **DeepSeek AI** -> **DeepSeek**

Anthropic models are often grouped with names such as **Haiku**, **Sonnet**, and **Opus**.

### 4.2 What makes frontier models impressive?

They are strong at:

- **Synthesizing information**: taking many ideas and turning them into one clear answer
- **Writing**: turning rough notes into emails, blog posts, study notes, or summaries
- **Coding**: writing, explaining, and debugging code

**Analogy:** They are like strong general-purpose helpers who can do many language tasks pretty well.

### 4.3 What are the limits?

Frontier models still have important limits.

- They are not true experts in every narrow field.
- Their knowledge can stop at a **training cutoff**, which means a date after which they may not know new facts.
- They can suggest old tools or old ways for programs to connect to each other, especially in coding.
- They can make mistakes and still sound very sure.

This is why human checking still matters.

**Quick recap:** Frontier models are top-level models from major labs. They are powerful, but they are not perfect and they can still be outdated or wrong.

---

## 5. Artificial neurons and neural networks

Before we explain transformers, we need two smaller building blocks.

### 5.1 What is an artificial neuron?

**What it is:** An **artificial neuron** is a tiny math unit inside a model.

**Why it exists:** Big models are built from many small parts. Each part does a simple job.

**How it works:** It takes in numbers, gives each one a different level of importance, mixes them, and produces an output number.

One of those importance numbers is called a **weight**. A **weight** tells the model how much one input should matter.

**Analogy:** Think of a small judge with many clues in front of it. Some clues matter more than others. The judge gives more weight to the important clues.

### 5.2 What is a neural network?

**What it is:** A **neural network** is a large group of artificial neurons connected together.

**Why it exists:** One tiny neuron can only do a very small job. Many neurons working together can learn complex patterns.

**How it works:** Neurons are arranged in **layers**. A **layer** is one row of many neurons. Early layers find simple patterns. Later layers combine those patterns into bigger ideas.

```text
Input -> [Layer 1] -> [Layer 2] -> [Layer 3] -> Output
```

**Analogy:** It is like a team project. One group notices simple clues. The next group combines them. The final group gives the answer.

### 5.3 Why is it called “neural”?

The name was inspired by the brain, but a neural network is not a real brain. It is a computer-made system that learns with math.

**Quick recap:** An artificial neuron is one small unit. A neural network is many small units working together in layers.

---

## 6. What “parameters” means

### 6.1 What is a parameter?

**What it is:** A **parameter** is one adjustable number inside a model.

**Why it exists:** The model needs many adjustable numbers so it can learn many patterns.

**How it works:** During training, the model changes these numbers little by little to get better.

**Analogy:** Parameters are like lots of tiny knobs. Training turns the knobs until the machine works better.

### 6.2 Why do people talk about parameter count?

People often say things like "7 billion parameters" or "70 billion parameters."

That number gives a rough idea of model size.

- More parameters can help the model learn more complex patterns.
- But more parameters also need more data, more training time, and more **compute**.

**Compute** means computer power and time.

### 6.3 Bigger is not always better

A bigger model is not automatically the best choice.

- Small models can be faster.
- Small models can be cheaper.
- Small models can be good enough for smaller tasks.

**Quick recap:** Parameters are adjustable inside numbers. More parameters can mean more possible power, but they also bring more cost.

---

## 7. From characters to words to tokens

This section matters a lot because transformers do not read full sentences the way humans do.

### 7.1 First idea: characters

A **character** is one letter, one number, one space, or one symbol.

Example:

```text
cat = c + a + t
```

Early language systems sometimes worked one character at a time.

**Why that was hard:** The model had to take many tiny steps, so learning long patterns was difficult.

### 7.2 Second idea: words

Later systems tried working one whole word at a time.

**Why that helped:** Words feel more natural to humans.

**Why that also caused problems:** Languages have many rare words, new words, names, spellings, and word forms.

### 7.3 Third idea: tokens

**What it is:** A **token** is a chunk of text.

**Why it exists:** Tokens are a useful middle ground between single characters and whole words.

**How it works:** A token can be:

- a full word
- part of a word
- punctuation
- a space-plus-word pattern

The exact split depends on the model's **tokenizer**.

A **tokenizer** is the tool that splits text into tokens and turns them into ID numbers.

**Analogy:** If words are full Lego models, tokens are Lego pieces. Some pieces are big. Some are small. You build with the pieces you have.

### 7.4 A simple token example

One tokenizer might split a long word like this:

```text
sunflower -> "sun" + "flower"
```

Another tokenizer might split it differently. The exact pieces can change from model to model.

### 7.5 Encoding and decoding

After text is split into tokens, each token gets a number ID.

- Turning text into token IDs is often called **encoding**.
- Turning token IDs back into text is often called **decoding**.

```text
Text -> Tokens -> Token IDs
Token IDs -> Tokens -> Text
```

### 7.6 What is `tiktoken`?

**What it is:** `tiktoken` is a Python library.

**Why it exists:** It helps developers count tokens and convert text to token IDs and back.

**How it works:** You give it text. It can encode the text into token IDs, count how many tokens there are, and decode the IDs back into text.

**Analogy:** It is like a helper that counts and labels the text pieces before the model sees them.

### 7.7 The big flow before we reach the transformer

```text
Your text
   ->
Tokenizer
   ->
Tokens
   ->
Token IDs
   ->
Model
```

In the next section, we will open up the "Model" box and see what happens inside.

**Quick recap:** Characters are tiny text units. Words are bigger text units. Tokens are flexible chunks. A tokenizer splits text into tokens and gives them number IDs.

---

## 8. The transformer, explained clearly

This is the most important technical section in the course, so we will go slowly.

### 8.1 What is a transformer?

**What it is:** A **transformer** is a model **architecture**. An **architecture** is the design or blueprint of the model.

**Why it exists:** Older systems had a harder time handling long text and large-scale training. The transformer gave the field a better design for language.

**How it works:** It processes tokens, compares them with one another using **attention**, which means noticing which parts matter most, and predicts the next token.

**Analogy:** If a model is a building, the transformer is the building plan.

In 2017, Google researchers published the famous transformer paper called **Attention Is All You Need**. That paper changed the direction of modern AI.

### 8.2 Two words we need first: sequence and embedding

Before we go further, we need two more simple terms.

**Sequence**

- A **sequence** is an ordered list.
- A sentence is a sequence of text pieces.
- Order matters.

Example:

```text
"The cat sat" != "Sat the cat"
```

**Embedding**

- An **embedding** is a list of numbers that represents a token in a way the model can work with.
- Tokens start as IDs, but IDs alone do not carry rich meaning.
- Embeddings give the model a more useful numeric form.

**Analogy for embeddings:** If a token ID is just a student's roll number, an embedding is a richer student profile card.

### 8.3 The step-by-step path inside a transformer

We will use this simple input:

```text
"The sky is"
```

#### Step 1: Split the text into tokens

The tokenizer breaks the text into pieces.

```text
"The sky is" -> ["The", " sky", " is"]
```

Do not worry if your own tokenizer shows slightly different pieces. Different models can split text in different ways.

#### Step 2: Turn tokens into token IDs

Each token becomes a number ID.

```text
["The", " sky", " is"] -> [101, 502, 88]
```

The exact numbers are just an example.

#### Step 3: Turn token IDs into embeddings

Now the model changes each token ID into an embedding.

Why? Because the model needs a richer numeric form than a plain label number.

```text
Token ID -> embedding
101      -> [many numbers]
502      -> [many numbers]
88       -> [many numbers]
```

#### Step 4: Add position information

The model also needs to know where each token is in the sequence.

Why? Because:

```text
"dog bites man"
```

is different from:

```text
"man bites dog"
```

So the model adds position clues to the embeddings.

**Analogy:** The words are not only students in a class. They also have seat numbers.

#### Step 5: Use attention

Now we reach the heart of the transformer.

**Attention** is a way for the model to decide which other tokens matter most for understanding the current token.

When the model looks at `"is"`, it may care a lot about `"sky"`.

```text
Tokens: [The] [sky] [is]
                 |
                 +---- pays strong attention to ----> [sky]
```

Another simple example:

```text
"The cat sat on the mat because it was soft."
```

To understand what `"it"` refers to, the model may pay more attention to `"mat"` than to `"cat"`.

This kind of token-to-token checking is often called **self-attention**.

**Self-attention** means the tokens in the same input look at one another.

#### Step 6: Repeat this in many layers

A transformer does not do attention only once.

It has many layers.

Each layer helps the model build a better understanding.

You can think of it like:

- first layer: notice simple relationships
- middle layers: combine ideas
- later layers: prepare for a strong prediction

#### Step 7: Predict the next token

After all this processing, the model predicts the next token.

For our example:

```text
"The sky is" -> maybe "blue"
```

#### Step 8: Add the new token and repeat

Once the model picks a token, it adds it to the sequence and does the process again.

```text
"The sky is" -> "blue"
"The sky is blue" -> maybe "today"
"The sky is blue today" -> maybe "."
```

That is how the model writes a full answer: one token at a time.

### 8.4 A full simple diagram

```text
Your sentence
   ->
Tokenizer
   ->
Tokens
   ->
Token IDs
   ->
Embeddings + position information
   ->
[Transformer layers]
   attention
   compare tokens
   build understanding
   ->
Next-token prediction
   ->
New token
   ->
Repeat until the answer is done
```

### 8.5 Why was the transformer such a big deal?

The transformer helped because it was very good at:

- handling sequences of text
- noticing which earlier parts matter
- growing to much larger sizes
- learning from more data and more compute in an efficient way

This is why people say the transformer made it easier to **scale**. To **scale** means to grow the system by using more data, more parameters, and more computer power.

### 8.6 Easy analogy for the whole transformer

Imagine a classroom discussion.

- The sentence is the whole class.
- Each token is one student.
- Each student can look around the room and notice which other students are most important right now.
- After several rounds of this, the class gives the next best answer.

**Quick recap:** A transformer is the blueprint used by modern LLMs. Text becomes tokens, tokens become embeddings, attention helps each token look at other useful tokens, and the model predicts the next token one step at a time.

---

## 9. LSTM and the short timeline of modern LLMs

### 9.1 What is LSTM?

**LSTM** stands for **long short-term memory**.

**What it is:** It is an older kind of neural network design for sequence data.

**Why it exists:** Before transformers became popular, researchers needed a way for models to carry some memory from earlier words to later words.

**How it works:** It reads the sequence step by step and passes a small memory state forward.

**Analogy:** It is like reading a sentence while carrying a small sticky note of what you think is important so far.

```text
Word 1 -> [LSTM memory] -> Word 2 -> [LSTM memory] -> Word 3 -> ...
```

### 9.2 Why do we hear more about transformers now?

Transformers usually worked better for very large language models.

They were better suited for large-scale training and long-range relationships in text.

That does not mean LSTM was useless. LSTM was an important step in the story.

### 9.3 Short timeline

- **2017**: Google researchers published the transformer paper.
- **2018**: OpenAI released **GPT-1**.
- **2019**: OpenAI released **GPT-2**.
- **2020**: OpenAI released **GPT-3**.
- **2022**: ChatGPT became widely known, helped by instruction tuning and RLHF.
- **2023**: GPT-4 and strong competitors pushed the frontier forward again.

```text
2017 -> Transformer
2018 -> GPT-1
2019 -> GPT-2
2020 -> GPT-3
2022 -> ChatGPT
2023 -> GPT-4 and strong rivals
```

**Quick recap:** LSTM is an older sequence model with a memory path. Transformers became the main design for large modern LLMs.

---

## 10. Prompt engineering, context engineering, RAG, and agentic AI

These four ideas are very important in real-world LLM work.

### 10.1 Prompt engineering

**What it is:** A **prompt** is the text you send to the model. **Prompt engineering** means writing that text in a clearer and smarter way.

**Why it exists:** The model can only respond to what it sees. Clear instructions usually lead to better answers.

**How it works:** You choose the right wording, examples, format, and level of detail.

**Analogy:** It is like asking a classmate for help. If your question is clear, the answer is more likely to be useful.

**Example:**

- Weak prompt: `Write code`
- Better prompt: `Write a Python function that reads a CSV file and prints the first five rows.`

### 10.2 Context engineering

**What it is:** **Context** means everything the model can see in one request.

That can include:

- the system instruction
- the user question
- older chat messages
- extra documents

**Context engineering** means choosing what to include, what to remove, and what to summarize.

**Why it exists:** Too little context can make the answer weak. Too much context can waste space and money.

**How it works:** You decide what information the model needs right now.

**Analogy:** It is like packing a school bag. You want the right books, not every book you own.

### 10.3 RAG

**RAG** stands for **retrieval-augmented generation**.

That sounds complex, so let us break it apart:

- **retrieval** = look up useful documents
- **augmented** = add those documents to the model's context
- **generation** = the model writes the answer

**What it is:** RAG is a method where the system finds useful documents first and then asks the model to answer using them.

**Why it exists:** A model's training data can be old or missing company-specific facts. RAG helps bring in fresh or private information.

**How it works:** Search first, add the best results to the prompt, then let the model answer.

```text
Question
   ->
Find useful documents
   ->
Add document snippets to the context
   ->
Model writes the answer
```

**Analogy:** It is like going to the library, finding the right pages, and then writing your answer with those pages open in front of you.

### 10.4 Agentic AI

**What it is:** **Agentic AI** means an AI system that can take several steps and use tools instead of giving only one direct reply.

**Why it exists:** Some tasks need actions, not just text.

**How it works:** The system can plan, use a tool, read the result, and choose the next step.

Examples of tools:

- search
- calendar
- code runner
- file reader

**Analogy:** A normal chatbot is like someone who only talks. An agent is like someone who can talk, look things up, and do small tasks.

**Mini example:** If you ask, "Book me a meeting," an agentic system might:

1. check the calendar
2. find free times
3. ask a follow-up question
4. book the meeting

**Quick recap:** Prompt engineering improves the question. Context engineering improves what the model can see. RAG adds looked-up documents. Agentic AI adds tools and multi-step action.

---

## 11. Why an API call is stateless, but chat still feels like memory

### 11.1 What is an API?

An **API** is a way for one program to talk to another program.

If your app sends a question to a model service on the internet, it usually does that through an API.

### 11.2 What does stateless mean?

**Stateless** means the server does not automatically remember your past conversation as a permanent personal memory for the next request.

Each request is treated like a fresh request.

**Analogy:** It is like meeting a teacher every day, but the teacher only knows what is written on the paper you hand over that day.

### 11.3 Then why does chat feel like memory?

Because your app usually stores the old messages and sends them again with the new message.

So the model does not remember by magic. The app keeps reminding it.

```text
Your app stores old messages
   ->
Sends old messages + new message
   ->
Model replies
```

This is the "impression of memory" from your notes.

### 11.4 Why this matters

If you forget to resend the old messages, the model may lose the thread of the conversation.

**Quick recap:** The API call is stateless. Chat feels like memory because the app sends the old conversation back again.

---

## 12. Context window and cost

### 12.1 What is a context window?

**What it is:** A **context window** is the maximum number of tokens the model can look at in one request.

**Why it exists:** The model cannot handle infinite text at once. It has a limit.

**How it works:** Your prompt, system message, old chat history, and extra documents all share that token space.

**Analogy:** It is like a desk with limited space. You can only spread out so many papers at once.

### 12.2 Why does a larger context window help?

A larger context window lets you include:

- longer conversations
- longer documents
- more retrieved notes

That can help the model refer back to more details from the current request.

But it still does not mean the model has true lifelong memory.

### 12.3 Why does cost go up?

Many model APIs charge based on:

- **input tokens**: the tokens you send in
- **output tokens**: the tokens the model sends back

So cost grows when you send:

- very long chat history
- large RAG document chunks
- long prompts
- long replies

This is why fake memory and RAG can raise the bill.

### 12.4 A simple rule

Good context engineering helps keep the context window useful and the cost under control.

**Quick recap:** The context window is the model's token limit for one request. More tokens usually mean more cost.

---

## 13. Python examples for calling OpenAI

This section matches the course notes and shows simple examples with `system`, `user`, `assistant`, and streaming.

Small note: OpenAI now recommends the newer **Responses API** for brand-new projects, but we use **Chat Completions** here because it is a very clear way to learn message roles and multi-turn chat. You can check the latest official guides here:

- [OpenAI quickstart](https://platform.openai.com/docs/quickstart?api-mode=responses&lang=python)
- [Chat Completions reference](https://platform.openai.com/docs/api-reference/chat/create?lang=python)
- [Streaming guide](https://platform.openai.com/docs/guides/streaming-responses?api-mode=chat)

### 13.1 Before you run the code

1. Install the OpenAI Python package:

```bash
pip install openai
```

2. Put your API key in an **environment variable**.

An **environment variable** is a secret value your program can read without typing it directly into the code file.

On macOS or Linux:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

3. Use a model name that supports chat completions. In these examples, we use `gpt-4.1-mini`.

### 13.2 Example A: `system` + `user`

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a kind tutor. Answer in 3 short sentences or fewer.",
        },
        {
            "role": "user",
            "content": "What is a language model, in very simple words?",
        },
    ],
)

print(response.choices[0].message.content)
```

### 13.3 Example B: `user` only

You can also make a simple request with only a user message.

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Give one example of a token that is not a full English word.",
        }
    ],
)

print(response.choices[0].message.content)
```

### 13.4 Example C: multi-turn chat with an old assistant message

This is how chat keeps context. Your code stores old messages and sends them back.

```python
from openai import OpenAI

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are a helpful study coach.",
    },
    {
        "role": "user",
        "content": "Teach me what attention means in a transformer, like I am 12.",
    },
    {
        "role": "assistant",
        "content": "Attention is like highlighting the important words so the model knows what matters most.",
    },
    {
        "role": "user",
        "content": "Now give me a one-line recap.",
    },
]

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
)

print(response.choices[0].message.content)
```

If you want another turn after this, you would add the new assistant reply to the list and send the full list again.

### 13.5 Example D: streaming

**Streaming** means you receive the answer in small pieces as it is being generated.

Why is that useful? Because the user can start reading before the whole answer is finished.

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4.1-mini",
    stream=True,
    messages=[
        {"role": "system", "content": "You explain things simply."},
        {"role": "user", "content": "Explain RAG in two short paragraphs."},
    ],
)

for chunk in stream:
    piece = chunk.choices[0].delta.content
    if piece is not None:
        print(piece, end="")

print()
```

### 13.6 Safety reminder

Your API key is like a password.

- Do not put it in public code.
- Do not put it in screenshots.
- Do not commit it to Git.

**Quick recap:** You can call OpenAI with `system`, `user`, and `assistant` messages. Multi-turn chat works by resending old messages. Streaming sends the answer a little at a time.

---

## 14. Final recap

You have now walked through the core ideas behind LLMs.

- A **model** learns from examples.
- A **language model** works with text.
- An **LLM** is a very large language model that predicts the next token again and again.
- **Base models** mainly continue text.
- **Chat or instruct models** are trained to answer like assistants.
- **Reasoning models** spend more effort on harder tasks.
- **Hybrid models** mix strengths from different styles.
- **Frontier models** are the strongest major models available at a given time, but they can still be wrong or outdated.
- **Artificial neurons** are small units, and **neural networks** are many of them working together.
- **Parameters** are adjustable inside numbers learned during training.
- **Tokens** are chunks of text, and a **tokenizer** splits text into those chunks.
- A **transformer** turns tokens into embeddings, uses attention to compare them, and predicts the next token.
- **LSTM** is an older sequence model that carries a small memory forward step by step.
- **Prompt engineering** improves the question.
- **Context engineering** improves what the model sees.
- **RAG** looks up documents first and then answers with those documents in hand.
- **Agentic AI** uses tools and multiple steps.
- An API call is **stateless**, so chat memory usually comes from resending old messages.
- The **context window** is the token limit for one request.
- More tokens usually mean more cost.

If you now go back to the original [notes.md](../../notes.md), the short points there should make much more sense.

---

*This document is part of the "LLM Fundamentals & Engineering" course materials. It expands classroom notes into a full beginner-friendly guide.*
