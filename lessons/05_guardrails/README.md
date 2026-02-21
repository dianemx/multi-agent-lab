# Lesson 05 — Guardrails

## Goal
Add **safety checks** that validate inputs and outputs of your agents.

## Key Concepts

- **Input Guardrails** — run BEFORE the agent processes the message. Can reject harmful/off-topic inputs.
- **Output Guardrails** — run AFTER the agent responds. Can catch inappropriate or incorrect outputs.
- Guardrails use a **secondary agent** to do the checking (an LLM judging another LLM).
- If a guardrail fails, it raises an exception you can catch and handle.

## Why guardrails matter

In production multi-agent systems, you need safety nets:
- Prevent prompt injection
- Keep agents on-topic
- Ensure output quality
- Block sensitive information leakage

## The flow

```
User message
    ↓
┌──────────────────┐
│ Input Guardrail   │ → ❌ Block  (raises InputGuardrailTripwireTriggered)
│ (check agent)     │ → ✅ Pass
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Main Agent       │
└──────┬───────────┘
       ↓
┌──────────────────┐
│ Output Guardrail  │ → ❌ Block  (raises OutputGuardrailTripwireTriggered)
│ (check agent)     │ → ✅ Pass
└──────┬───────────┘
       ↓
  Final output (safe & validated)
```

## Run it

```bash
python main.py
```

## Exercises
1. Add a guardrail that blocks requests in languages other than English
2. Create an output guardrail that checks for PII (personal information)
3. Combine guardrails with handoffs from Lesson 04
