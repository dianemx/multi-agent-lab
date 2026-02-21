# Lesson 02 — Tools

## Goal
Give your agent **capabilities** by defining Python functions as tools.

## Key Concepts

- **`@function_tool`** — a decorator that turns any Python function into a tool the agent can call.
- The agent sees the function's **name**, **docstring**, and **parameter types** (via type hints).
- The agent **decides** when to call a tool based on the user's request.

## How the agent loop works with tools

```
User message
    ↓
┌─────────────┐
│   Agent      │ ← instructions + tool definitions
│   (LLM)      │
└─────┬───────┘
      │ decides to call a tool
      ↓
┌─────────────┐
│  Tool Call   │ → Python function executes
└─────┬───────┘
      │ result sent back to LLM
      ↓
┌─────────────┐
│   Agent      │ ← now has the tool result
│   (LLM)      │
└─────┬───────┘
      │
      ↓
  Final text output (incorporates tool results)
```

The LLM can call **multiple tools** in sequence before producing a final answer.

## Run it

```bash
python main.py
```

## Exercises
1. Add a `get_time()` tool that returns the current time
2. Make a tool that takes two parameters (e.g., `convert_currency(amount, from_currency, to_currency)`)
3. Ask a question that requires calling multiple tools in sequence
