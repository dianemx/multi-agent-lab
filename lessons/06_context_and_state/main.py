"""
Lesson 06 — Context & State
==============================
Share a typed context object across agents, tools, and handoffs.

Key takeaways:
  • Define a context class (dataclass or Pydantic model) with whatever state you need.
  • Pass it to Runner.run(..., context=my_context).
  • Tools access it via the RunContextWrapper parameter (ctx.context).
  • All agents in a handoff chain share the SAME context object.
  • This is how agents pass data to each other without relying on conversation text.
"""

import asyncio
import os
import sys
from dataclasses import dataclass, field

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from agents import Agent, Runner, RunContextWrapper, function_tool


# ── Step 1: Define a context class ──────────────────────────────────
# This holds all the shared state for one conversation/run.
@dataclass
class UserContext:
    user_name: str
    user_language: str = "English"
    interests: list[str] = field(default_factory=list)
    # Agents/tools can write to this during execution
    recommendations: list[str] = field(default_factory=list)
    search_history: list[str] = field(default_factory=list)


# ── Step 2: Define tools that READ and WRITE context ────────────────
# The first parameter (ctx) is automatically injected by the SDK.
# ctx.context gives you the UserContext instance.

@function_tool
def save_interest(ctx: RunContextWrapper[UserContext], interest: str) -> str:
    """Record a user interest for future reference.

    Args:
        interest: The topic or interest to save.
    """
    ctx.context.interests.append(interest)
    return f"Saved interest: {interest}. Total interests: {len(ctx.context.interests)}"


@function_tool
def save_recommendation(ctx: RunContextWrapper[UserContext], recommendation: str) -> str:
    """Save a recommendation that was made to the user.

    Args:
        recommendation: The recommendation text to save.
    """
    ctx.context.recommendations.append(recommendation)
    return f"Recommendation saved. Total: {len(ctx.context.recommendations)}"


@function_tool
def get_user_profile(ctx: RunContextWrapper[UserContext]) -> str:
    """Get the current user's profile information."""
    c = ctx.context
    return (
        f"Name: {c.user_name}\n"
        f"Language: {c.user_language}\n"
        f"Interests: {', '.join(c.interests) if c.interests else 'None yet'}\n"
        f"Past recommendations: {len(c.recommendations)}"
    )


@function_tool
def search_books(ctx: RunContextWrapper[UserContext], query: str) -> str:
    """Search for books on a topic (simulated).

    Args:
        query: The search query.
    """
    # Record the search in context
    ctx.context.search_history.append(query)

    # Simulated results
    fake_results = {
        "python": ["Fluent Python", "Python Cookbook", "Automate the Boring Stuff"],
        "ai": ["Life 3.0", "Superintelligence", "The Alignment Problem"],
        "cooking": ["Salt Fat Acid Heat", "The Food Lab", "On Food and Cooking"],
    }
    # Find matching results
    for keyword, books in fake_results.items():
        if keyword in query.lower():
            return f"Found books about {query}: {', '.join(books)}"
    return f"No books found for '{query}'. Try: python, ai, or cooking."


# ── Step 3: Create agents that use context-aware tools ───────────────
librarian = Agent(
    name="Librarian",
    instructions=(
        "You are a helpful librarian. "
        "ALWAYS start by checking the user's profile with get_user_profile. "
        "Use the user's name when addressing them. "
        "Search for books based on their interests, and save any recommendations you make. "
        "Also save any new interests the user mentions."
    ),
    model=MODEL,
    tools=[get_user_profile, search_books, save_interest, save_recommendation],
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 06 — Context & State")
    print("=" * 60)

    # Create a context object — this persists across the entire run
    user_ctx = UserContext(
        user_name="Antonio",
        user_language="English",
        interests=["Python", "architecture"],
    )

    # ── First conversation ───────────────────────────────────────────
    print("\n📖 First question:")
    q1 = "I'm interested in learning AI. Can you recommend some books?"
    print(f"🧑 {q1}\n")

    result = await Runner.run(librarian, q1, context=user_ctx)
    print(f"🤖 Librarian: {result.final_output}")

    # Check what happened to our context
    print("\n📊 Context after first run:")
    print(f"   Interests:       {user_ctx.interests}")
    print(f"   Recommendations: {user_ctx.recommendations}")
    print(f"   Search history:  {user_ctx.search_history}")

    # ── Second conversation — context PERSISTS ───────────────────────
    print("\n" + "=" * 60)
    print("📖 Second question (note: context carries over):")
    q2 = "What about cooking books? I've started learning to cook."
    print(f"🧑 {q2}\n")

    result = await Runner.run(librarian, q2, context=user_ctx)
    print(f"🤖 Librarian: {result.final_output}")

    # Context has accumulated data from BOTH runs
    print("\n📊 Context after second run:")
    print(f"   Interests:       {user_ctx.interests}")
    print(f"   Recommendations: {user_ctx.recommendations}")
    print(f"   Search history:  {user_ctx.search_history}")


if __name__ == "__main__":
    asyncio.run(main())
