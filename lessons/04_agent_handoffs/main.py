"""
Lesson 04 — Agent Handoffs
============================
The core multi-agent pattern: agents delegate to specialists.

Key takeaways:
  • handoffs=[agent_b] lets agent_a transfer control to agent_b.
  • The LLM decides WHEN to hand off (based on instructions + handoff descriptions).
  • After handoff, the NEW agent takes over the conversation.
  • You can inspect result.last_agent to see WHO produced the final answer.

Think of it like a call center: a triage operator identifies what you need,
then transfers you to the right department.
"""

import asyncio
import os
import sys

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from agents import Agent, Runner


# ── Define specialist agents ────────────────────────────────────────
# Each specialist handles a specific domain.

tech_support = Agent(
    name="Tech Support Specialist",
    instructions=(
        "You are a technical support specialist. "
        "Help users with software bugs, installation issues, and technical problems. "
        "Be patient and provide step-by-step solutions. "
        "If the issue is about billing, tell the user you'll transfer them."
    ),
    model=MODEL,
    # This description is shown to the triage agent to help it decide
    handoff_description="Handles technical issues: bugs, setup, errors, how-to questions",
)

billing_support = Agent(
    name="Billing Specialist",
    instructions=(
        "You are a billing specialist. "
        "Help users with invoices, payments, refunds, and subscription changes. "
        "Be professional and clear about any costs involved."
    ),
    model=MODEL,
    handoff_description="Handles billing: invoices, payments, refunds, subscriptions",
)

general_support = Agent(
    name="General Support",
    instructions=(
        "You are a general support agent. "
        "Help with any questions that don't fit into tech or billing. "
        "Be friendly and helpful. If the question is technical or about billing, "
        "let the user know you'll transfer them."
    ),
    model=MODEL,
    handoff_description="Handles general inquiries, feedback, and other questions",
)


# ── Define the triage agent (the router) ────────────────────────────
# This agent doesn't answer questions itself — it routes to specialists.

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support triage agent. "
        "Your ONLY job is to understand the user's issue and transfer them "
        "to the right specialist. Do NOT try to solve the problem yourself. "
        "Briefly acknowledge the user's issue, then hand off immediately."
    ),
    model=MODEL,
    handoffs=[tech_support, billing_support, general_support],
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 04 — Agent Handoffs")
    print("=" * 60)

    # Different questions should route to different specialists
    questions = [
        "I keep getting a 'connection refused' error when starting the app",
        "I was charged twice for my monthly subscription",
        "What are your office hours?",
    ]

    for q in questions:
        print(f"\n🧑 Customer: {q}")
        print("-" * 40)

        result = await Runner.run(triage_agent, q)

        # result.last_agent tells us which agent produced the final answer
        print(f"📋 Handled by: {result.last_agent.name}")
        print(f"🤖 Response: {result.final_output}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
