# Lesson 06 — Context & State

## Goal
Share **state** across agents and tools using a typed context object.

## Key Concepts

- **Context** — a user-defined object (dataclass or Pydantic model) shared across the entire agent run.
- Pass it to `Runner.run(agent, input, context=my_context)`.
- Tools receive it via `RunContextWrapper` — they can both **read** and **mutate** it.
- All agents in a handoff chain share the **same context instance**.

## Why context matters

In multi-agent systems, agents need shared state:
- A researcher agent finds data → stores it in context → writer agent uses it
- A tool records every action → context accumulates an audit log
- User preferences set once → accessible by all agents

## Diagram

```
             context (shared state)
                  │
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
┌────────┐  ┌────────┐  ┌────────┐
│ Agent A │  │ Agent B │  │ Tool 1 │
│ (reads) │  │ (reads) │  │(writes)│
└────────┘  └────────┘  └────────┘
```

## Run it

```bash
python main.py
```

## Exercises
1. Add a field to track how many tool calls were made during the conversation
2. Create a "memory" field where agents can store notes for each other
3. Add a second agent that reads data the first agent's tools stored
