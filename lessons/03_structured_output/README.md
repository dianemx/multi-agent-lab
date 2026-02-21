# Lesson 03 — Structured Output

## Goal
Force an agent to return a **typed, validated object** instead of free-form text.

## Key Concepts

- **`output_type`** — set this on an Agent to a Pydantic model, and the agent MUST return data matching that schema.
- The LLM sees the JSON schema and produces structured JSON.
- The SDK validates it automatically against your Pydantic model.
- This is essential for **agentic pipelines** where one agent's output feeds into another.

## Why this matters

Free-form text is great for chatbots, but in multi-agent systems you need **reliable data flow** between agents. Structured output guarantees:
- The output matches a known schema
- You can access fields directly (no parsing needed)
- Downstream agents/code can depend on the structure

## Run it

```bash
python main.py
```

## Exercises
1. Add more fields to `MovieRecommendation` (e.g., `director`, `year`)
2. Create a `CodeReview` model with fields like `issues`, `suggestions`, `score`
3. Make an agent that outputs a `List[...]` (hint: wrap it in a Pydantic model with a list field)
