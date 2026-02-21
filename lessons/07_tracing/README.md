# Lesson 07 — Tracing & Observability

## Goal
Understand what's happening inside your agent runs with **built-in tracing**.

## Key Concepts

- **Tracing** — the SDK automatically records every step: LLM calls, tool executions, handoffs, guardrail checks.
- **`trace()`** — context manager to create a named trace span around a block of work.
- Traces can be viewed in the **OpenAI dashboard** or exported for custom logging.
- Essential for **debugging** when agents make unexpected decisions.

## Why tracing matters

Multi-agent systems are hard to debug because:
- Multiple LLM calls happen in sequence
- Handoffs move control between agents
- Tools execute Python code between LLM calls
- You need to see the full chain to understand what happened

## Run it

```bash
python main.py
```

This lesson:
- Shows how to wrap agent runs in named traces
- Demonstrates custom trace processing
- Prints a structured log of every step

## Exercises
1. Run a multi-agent handoff from Lesson 04 and inspect the trace
2. Add custom metadata to trace spans
3. View traces in the OpenAI dashboard (platform.openai.com)
