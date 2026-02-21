"""
Lesson 02 — Tools
==================
Agents become powerful when they can DO things.
Tools are plain Python functions that the agent can choose to call.

Key takeaways:
  • Decorate a function with @function_tool to make it available to an agent.
  • The function's docstring and type hints tell the LLM what the tool does.
  • The agent decides WHEN and WHETHER to call each tool.
  • The Runner executes the function and feeds the result back to the LLM.
"""

import asyncio
import os
import sys
import random
from datetime import datetime

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from agents import Agent, Runner, function_tool


# ── Define tools ─────────────────────────────────────────────────────
# A tool is just a Python function with a docstring and type hints.
# The @function_tool decorator registers it so the agent can use it.


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to check weather for.
    """
    # In a real app, you'd call a weather API here.
    # For learning, we'll return mock data.
    conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    temp = random.randint(-5, 35)
    condition = random.choice(conditions)
    return f"Weather in {city}: {temp}°C, {condition}"


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result.

    Args:
        expression: A math expression like '2 + 2' or '(10 * 5) / 3'.
    """
    try:
        # WARNING: eval() is dangerous in production! This is just for learning.
        # In a real app, use a safe math parser.
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@function_tool
def get_current_date() -> str:
    """Get today's date and day of the week."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y — %H:%M")


# ── Define the agent with tools ─────────────────────────────────────
agent = Agent(
    name="Tool-Equipped Assistant",
    instructions=(
        "You are a helpful assistant with access to tools. "
        "Use the available tools when the user's question requires them. "
        "Always report tool results clearly."
    ),
    model=MODEL,
    tools=[get_weather, calculate, get_current_date],
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 02 — Tools")
    print("=" * 60)

    # This question should trigger the weather tool
    questions = [
        "What's the weather like in Rome and Tokyo?",
        "What is 42 * 17 + 3?",
        "What day is it today, and what's the weather in Milan?",
    ]

    for q in questions:
        print(f"\n🧑 You: {q}")
        result = await Runner.run(agent, q)
        print(f"🤖 Agent: {result.final_output}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())
