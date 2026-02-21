"""
Lesson 05 — Guardrails
========================
Safety checks for agent inputs and outputs.

Key takeaways:
  • InputGuardrail runs a checker agent BEFORE the main agent processes input.
  • OutputGuardrail runs a checker agent AFTER the main agent responds.
  • If the guardrail's output.tripwire_triggered is True, the SDK raises an exception.
  • You catch InputGuardrailTripwireTriggered / OutputGuardrailTripwireTriggered.
  • The checker agent uses structured output to make a clear pass/fail decision.
"""

import asyncio
import os
import sys

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from pydantic import BaseModel, Field
from agents import (
    Agent,
    Runner,
    InputGuardrail,
    OutputGuardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)


# ── Step 1: Define schemas for guardrail decisions ──────────────────
class TopicCheck(BaseModel):
    """Result of checking if a message is on-topic."""

    is_on_topic: bool = Field(description="True if the message is about cooking/food")
    reasoning: str = Field(description="Brief explanation of the decision")


class ToxicityCheck(BaseModel):
    """Result of checking if output contains toxic content."""

    is_toxic: bool = Field(description="True if the text contains toxic/harmful content")
    reasoning: str = Field(description="Brief explanation")


# ── Step 2: Create guardrail checker agents ──────────────────────────
# These are lightweight agents whose ONLY job is to classify/check.

topic_checker = Agent(
    name="Topic Checker",
    instructions=(
        "Determine if the user's message is related to cooking, recipes, or food. "
        "Messages asking about restaurants, ingredients, or cooking techniques are ON topic. "
        "Everything else is OFF topic."
    ),
    model=MODEL,
    output_type=TopicCheck,
)

toxicity_checker = Agent(
    name="Toxicity Checker",
    instructions=(
        "Check if the given text contains toxic, harmful, or offensive content. "
        "Be reasonable — normal cooking instructions (e.g., using knives, heat) are fine."
    ),
    model=MODEL,
    output_type=ToxicityCheck,
)


# ── Step 3: Create guardrail functions ───────────────────────────────
# These functions connect the checker agents to the guardrail system.

async def check_topic(ctx, agent, input) -> GuardrailFunctionOutput:
    """Input guardrail: ensures the user is asking about cooking."""
    result = await Runner.run(topic_checker, input, context=ctx.context)
    check = result.final_output  # a TopicCheck instance

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=not check.is_on_topic,  # trigger if OFF topic
    )


async def check_toxicity(ctx, agent, output) -> GuardrailFunctionOutput:
    """Output guardrail: ensures the agent's response is not toxic."""
    result = await Runner.run(toxicity_checker, output, context=ctx.context)
    check = result.final_output  # a ToxicityCheck instance

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=check.is_toxic,  # trigger if toxic
    )


# ── Step 4: Create the main agent WITH guardrails ───────────────────
cooking_agent = Agent(
    name="Chef Assistant",
    instructions=(
        "You are a friendly cooking assistant. "
        "Help users with recipes, cooking techniques, and food-related questions. "
        "Give concise, practical answers."
    ),
    model=MODEL,
    input_guardrails=[
        InputGuardrail(guardrail_function=check_topic),
    ],
    output_guardrails=[
        OutputGuardrail(guardrail_function=check_toxicity),
    ],
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 05 — Guardrails")
    print("=" * 60)

    test_messages = [
        # ✅ On-topic — should pass input guardrail
        "How do I make a perfect risotto?",
        # ❌ Off-topic — should be blocked by input guardrail
        "Can you help me write a Python script?",
        # ✅ On-topic
        "What's a good substitute for eggs in baking?",
    ]

    for msg in test_messages:
        print(f"\n🧑 You: {msg}")
        print("-" * 40)

        try:
            result = await Runner.run(cooking_agent, msg)
            print(f"✅ Agent: {result.final_output}")

        except InputGuardrailTripwireTriggered as e:
            print(f"🚫 BLOCKED (input guardrail): Message was off-topic")
            # In a real app, you'd return a friendly "I can only help with cooking" message

        except OutputGuardrailTripwireTriggered as e:
            print(f"🚫 BLOCKED (output guardrail): Response flagged as inappropriate")

        print()


if __name__ == "__main__":
    asyncio.run(main())
