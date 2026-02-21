# Multi-Agent Lab 🧪

A hands-on learning path for building multi-agent AI applications using the **OpenAI Agents SDK**.

## Prerequisites

- Python 3.12+
- An **Azure OpenAI** resource with a GPT-4o deployment
- Basic Python knowledge

## Quick Start

```bash
# 1. Create a virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Azure OpenAI
copy .env.example .env
# Edit .env and fill in your Azure OpenAI endpoint, key, and deployment name

# 4. Start with Lesson 01
cd lessons/01_hello_agent
python main.py
```

## Learning Path

| # | Lesson | What You'll Learn |
|---|--------|-------------------|
| 01 | [Hello Agent](lessons/01_hello_agent/) | Create your first agent, run it, understand the basics |
| 02 | [Tools](lessons/02_tools/) | Give agents capabilities with function tools |
| 03 | [Structured Output](lessons/03_structured_output/) | Get typed, validated responses from agents |
| 04 | [Agent Handoffs](lessons/04_agent_handoffs/) | Multiple agents collaborating via handoffs |
| 05 | [Guardrails](lessons/05_guardrails/) | Input/output validation and safety checks |
| 06 | [Context & State](lessons/06_context_and_state/) | Share state across agents and tools |
| 07 | [Tracing](lessons/07_tracing/) | Observability, debugging, and logging |

## Final Project

After completing the lessons, build and explore the **Content Research & Writing Team** — a fully orchestrated multi-agent system:

➡️ [Final Project: Multi-Agent Content Team](project/)

## Key Concepts

### What is an Agent?
An agent is an LLM configured with **instructions** (system prompt), **tools** (functions it can call), and **handoffs** (other agents it can delegate to).

### What is the Agents SDK?
OpenAI's lightweight Python framework for building agentic applications. It provides:
- **Agent loop** — the LLM runs in a loop, calling tools and making decisions until it produces a final output
- **Handoffs** — agents can transfer control to other agents
- **Guardrails** — validate inputs/outputs to keep agents on track
- **Tracing** — built-in observability for debugging and monitoring

### How does it differ from LangChain / CrewAI?
- **Minimal abstraction** — you're close to the metal, easy to understand what's happening
- **First-party** — built by OpenAI, tight integration with their models
- **Pythonic** — uses standard patterns (async/await, Pydantic, decorators)
