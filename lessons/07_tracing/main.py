"""
Lesson 07 — Tracing & Observability
=====================================
See what's happening inside agent runs with built-in tracing.

Key takeaways:
  • The SDK automatically traces every agent run (LLM calls, tool calls, handoffs).
  • Use trace("name") as a context manager to group related work.
  • Traces appear in the OpenAI dashboard at platform.openai.com > Traces.
  • You can also capture traces locally for custom logging/debugging.
  • result.raw_responses gives you low-level details of LLM calls.
"""

import asyncio
import os
import sys

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from agents import Agent, Runner, function_tool, trace


# ── Tools ────────────────────────────────────────────────────────────
@function_tool
def lookup_capital(country: str) -> str:
    """Look up the capital city of a country.

    Args:
        country: The country name.
    """
    capitals = {
        "france": "Paris",
        "japan": "Tokyo",
        "brazil": "Brasilia",
        "italy": "Rome",
        "australia": "Canberra",
    }
    result = capitals.get(country.lower(), f"Unknown capital for {country}")
    return f"The capital of {country} is {result}"


@function_tool
def lookup_population(city: str) -> str:
    """Look up the approximate population of a city.

    Args:
        city: The city name.
    """
    populations = {
        "paris": "2.1 million",
        "tokyo": "14 million",
        "rome": "2.8 million",
        "brasilia": "3.0 million",
        "canberra": "460,000",
    }
    result = populations.get(city.lower(), f"Unknown population for {city}")
    return f"Population of {city}: {result}"


# ── Agent ────────────────────────────────────────────────────────────
geography_agent = Agent(
    name="Geography Expert",
    instructions=(
        "You are a geography expert. Use your tools to look up information. "
        "Always use the tools rather than relying on memory."
    ),
    model=MODEL,
    tools=[lookup_capital, lookup_population],
)


# ── Run with tracing ────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 07 — Tracing & Observability")
    print("=" * 60)

    # ── Method 1: Automatic tracing (every Runner.run is traced) ─────
    print("\n📍 Run 1: Automatic tracing")
    print("-" * 40)

    result = await Runner.run(
        geography_agent,
        "What's the capital of France, and what's its population?",
    )
    print(f"🤖 {result.final_output}")

    # ── Method 2: Named trace span for grouping ─────────────────────
    # Use trace() to create a named span — useful for grouping
    # multiple agent runs that belong to the same logical operation.
    print("\n📍 Run 2: Named trace span ('geography-quiz')")
    print("-" * 40)

    with trace("geography-quiz"):
        # These two runs will appear under one trace in the dashboard
        r1 = await Runner.run(
            geography_agent, "What's the capital of Japan?"
        )
        print(f"🤖 Q1: {r1.final_output}")

        r2 = await Runner.run(
            geography_agent,
            f"And what about Italy? Compare its capital's population with Japan's capital.",
        )
        print(f"🤖 Q2: {r2.final_output}")

    # ── Inspecting the run result ────────────────────────────────────
    print("\n📊 Inspecting last run result:")
    print("-" * 40)
    print(f"  Last agent: {result.last_agent.name}")

    # raw_responses contains the actual OpenAI API responses
    print(f"  Number of LLM calls: {len(result.raw_responses)}")
    for i, response in enumerate(result.raw_responses):
        usage = response.usage
        print(f"  Call {i+1}: {usage.input_tokens} input tokens, {usage.output_tokens} output tokens")

    # ── Tip: View in OpenAI Dashboard ────────────────────────────────
    print("\n💡 Tip: View your traces at:")
    print("   https://platform.openai.com/traces")
    print("   You'll see each agent run with all LLM calls, tool calls, and decisions.")


if __name__ == "__main__":
    asyncio.run(main())
