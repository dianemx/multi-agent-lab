# Lesson 04 — Agent Handoffs

## Goal
Build a **multi-agent** system where agents can delegate work to each other.

## Key Concepts

- **Handoff** — an agent can transfer the conversation to another, more specialized agent.
- You configure handoffs in the `handoffs` parameter of `Agent()`.
- The LLM decides when to hand off based on the agent's instructions and the handoff descriptions.
- This is the **core multi-agent pattern**: a triage/router agent delegates to specialists.

## The Handoff Pattern

```
User message
    ↓
┌─────────────────┐
│  Triage Agent    │ ← "Route to the right specialist"
└─────┬───────────┘
      │ handoff decision
      ├──────────────────┐──────────────────┐
      ↓                  ↓                  ↓
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Tech      │      │ Billing  │      │ General  │
│ Support   │      │ Support  │      │ Support  │
└──────────┘      └──────────┘      └──────────┘
```

The triage agent sees the user's message and decides which specialist should handle it.
After handoff, the **specialist** takes over and produces the final output.

## Run it

```bash
python main.py
```

## Exercises
1. Add a fourth specialist (e.g., "Sales Agent")
2. Create a chain: Agent A → Agent B → Agent C (multi-hop handoff)
3. Give one of the specialists a tool, combining handoffs + tools
