# Lesson 01 — Hello Agent

## Goal
Create your very first AI agent and have a conversation with it.

## Key Concepts
- **`Agent`** — the core building block. An LLM + instructions + (optionally) tools and handoffs.
- **`Runner.run()`** — executes the agent loop: sends messages to the LLM, processes tool calls, repeats until the agent produces a final text output.
- **Instructions** — the system prompt that shapes the agent's behavior.

## What happens when you run an agent?

```
User message
    ↓
┌─────────────┐
│   Agent      │ ← instructions (system prompt)
│   (LLM)      │
└─────┬───────┘
      │
      ↓
  Final text output
```

The Runner sends your message to the LLM along with the agent's instructions.
The LLM generates a response. Since this agent has no tools, it produces a final
text output directly.

## Run it

```bash
python main.py
```

## Exercises
1. Change the agent's instructions to make it a pirate 🏴‍☠️
2. Change the model to `gpt-4o-mini` and compare the output
3. Try passing a multi-turn conversation (list of messages)
