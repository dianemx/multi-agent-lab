"""
Multi-Agent Content Team — Main Entry Point
=============================================
Runs the full pipeline: Research → Write → Review

This demonstrates a SEQUENTIAL pipeline pattern:
  1. Orchestrator hands off to Researcher
  2. Then we run the Writer (with context from research)
  3. Then we run the Reviewer (which returns structured output)

Usage:
    python main.py                              # Default topic
    python main.py "The future of renewable energy"   # Custom topic
"""

import asyncio
import os
import sys
from dataclasses import dataclass, field

# Add project root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import MODEL  # loads .env and sets up Azure OpenAI
from agents import Runner, trace
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from project.agents.researcher import researcher
from project.agents.writer import writer
from project.agents.reviewer import reviewer


# ── Shared context for the entire pipeline ───────────────────────────
@dataclass
class PipelineContext:
    """Shared state across all agents in the pipeline."""

    topic: str = ""
    research: dict = field(default_factory=dict)
    draft: str = ""
    draft_version: int = 0


# ── Main pipeline ───────────────────────────────────────────────────
async def run_pipeline(topic: str):
    console = Console()

    # Create shared context
    ctx = PipelineContext(topic=topic)

    console.print(Panel(f"[bold]Topic:[/bold] {topic}", title="🚀 Content Pipeline", border_style="blue"))

    # ── Phase 1: Research ────────────────────────────────────────────
    with trace("Phase 1: Research"):
        console.print("\n[bold cyan]Phase 1: Research[/bold cyan]")
        console.print("Handing off to the Researcher agent...\n")

        result = await Runner.run(
            researcher,
            f"Research the following topic thoroughly: {topic}",
            context=ctx,
        )
        console.print(f"[green]✓ Research complete[/green]")
        console.print(f"  Topics researched: {list(ctx.research.keys())}")
        console.print(f"  Handled by: {result.last_agent.name}")

    # ── Phase 2: Writing ─────────────────────────────────────────────
    with trace("Phase 2: Writing"):
        console.print("\n[bold cyan]Phase 2: Writing[/bold cyan]")
        console.print("Handing off to the Writer agent...\n")

        result = await Runner.run(
            writer,
            f"Write a compelling article about: {topic}. Use the research that has been gathered.",
            context=ctx,
        )
        console.print(f"[green]✓ Draft v{ctx.draft_version} complete[/green]")
        console.print(f"  Draft length: {len(ctx.draft)} characters")

    # ── Phase 3: Review ──────────────────────────────────────────────
    with trace("Phase 3: Review"):
        console.print("\n[bold cyan]Phase 3: Review[/bold cyan]")
        console.print("Handing off to the Reviewer agent...\n")

        result = await Runner.run(
            reviewer,
            f"Review the current draft about: {topic}",
            context=ctx,
        )
        review = result.final_output  # This is a ContentReview Pydantic model

        console.print(f"[green]✓ Review complete[/green]")

    # ── Display results ──────────────────────────────────────────────
    console.print("\n" + "=" * 70)
    console.print(Panel(Markdown(ctx.draft), title="📄 Final Article", border_style="green"))

    console.print(Panel(
        f"[bold]Score:[/bold] {review.overall_score}/10\n"
        f"[bold]Verdict:[/bold] {review.verdict}\n\n"
        f"[bold]Summary:[/bold] {review.summary}\n\n"
        f"[bold green]Strengths:[/bold green]\n" +
        "\n".join(f"  • {s}" for s in review.strengths) +
        f"\n\n[bold yellow]Weaknesses:[/bold yellow]\n" +
        "\n".join(f"  • {w}" for w in review.weaknesses) +
        f"\n\n[bold blue]Suggestions:[/bold blue]\n" +
        "\n".join(f"  • {s}" for s in review.suggestions),
        title="📝 Review",
        border_style="yellow",
    ))

    console.print("\n💡 [dim]View traces at: https://platform.openai.com/traces[/dim]")

    return ctx, review


# ── Entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "quantum computing"

    asyncio.run(run_pipeline(topic))
