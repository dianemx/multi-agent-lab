"""
Lesson 01 — Hello Agent
========================
Your first agent: just an LLM with a personality.

Key takeaways:
  • Agent() defines WHO the agent is (name, instructions, model).
  • Runner.run() actually EXECUTES the agent and returns a result.
  • result.final_output contains the agent's text response.
"""

import asyncio
import os
import sys

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL  # ← Azure OpenAI model from shared config
from agents import Agent, Runner


# ── 1. Define the agent ──────────────────────────────────────────────
agent = Agent(
    name="Helpful Assistant",
    instructions=(
        "You are a friendly and concise assistant. "
        "When answering, get straight to the point. "
        "If you don't know something, say so honestly."
        "You were possessed by a pirate from the Caribbean, so feel free to sprinkle in pirate phrases like 'Ahoy' and 'Matey' when appropriate."
    ),
    model=MODEL,  # ← Uses your Azure OpenAI deployment
)


# ── 2. Run the agent ────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 01 — Hello Agent")
    print("=" * 60)

    # Ask a single question
    question = "What are the key differences between Python and Java?"
    print(f"\n🧑 You: {question}\n")

    result = await Runner.run(agent, question)

    print(f"🤖 Agent: {result.final_output}")

    # ── Bonus: multi-turn conversation ───────────────────────────────
    # Runner is already imported at the top — no need to import again.
    result = await Runner.run(agent, [
         {"role": "user", "content": "My name is Antonio."},
         {"role": "assistant", "content": "Nice to meet you, Antonio!"},
         {"role": "user", "content": "What's my name?"},
    ])
    print(result.final_output)  # → "Your name is Antonio."


if __name__ == "__main__":
    asyncio.run(main())
