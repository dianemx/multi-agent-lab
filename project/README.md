# Final Project — Multi-Agent Content Team

## Overview

A complete multi-agent system where specialized agents collaborate to **research, write, and review** content. This project combines ALL the concepts from the lessons:

- **Agents** (Lesson 01)
- **Tools** (Lesson 02)
- **Structured Output** (Lesson 03)
- **Handoffs** (Lesson 04)
- **Guardrails** (Lesson 05)
- **Context & State** (Lesson 06)
- **Tracing** (Lesson 07)

## Architecture

```
User request: "Write an article about quantum computing"
    │
    ↓
┌─────────────────────────────┐
│     Orchestrator Agent       │ ← Routes and coordinates
│     (triage + planning)      │
└──────┬──────────────────────┘
       │
       ├──→ 🔍 Researcher Agent        (gathers information using tools)
       │         │
       │         ↓ stores findings in shared context
       │
       ├──→ ✍️  Writer Agent            (creates content from research)
       │         │
       │         ↓ stores draft in shared context
       │
       └──→ 📝 Reviewer Agent          (reviews & provides feedback)
                 │
                 ↓ structured review with score
```

## Files

| File | Role |
|------|------|
| `main.py` | Entry point — runs the full pipeline |
| `agents/orchestrator.py` | The triage/coordinator agent |
| `agents/researcher.py` | Research agent + search tools |
| `agents/writer.py` | Content writing agent |
| `agents/reviewer.py` | Quality review agent (structured output) |
| `tools/web_search.py` | Simulated web search tool |
| `tools/file_tools.py` | File read/write tools |

## Run it

```bash
cd project
python main.py
```

You can also pass a custom topic:

```bash
python main.py "The future of renewable energy"
```

## How to extend this

- **Add a real search API** — replace the simulated search with Tavily, Brave, or SerpAPI
- **Add an editor agent** — rewrites based on reviewer feedback
- **Add a fact-checker** — verifies claims in the draft
- **Loop until quality** — have the orchestrator loop writer → reviewer until score > 8
