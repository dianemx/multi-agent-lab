"""
File tools for reading and writing content.

These tools let agents save their work (research notes, drafts, final articles)
to the shared context and optionally to disk.
"""

from agents import function_tool, RunContextWrapper


@function_tool
def save_research(ctx: RunContextWrapper, topic: str, findings: str) -> str:
    """Save research findings to shared context.

    Args:
        topic: The research topic or subtopic.
        findings: The research findings/notes to save.
    """
    if not hasattr(ctx.context, "research"):
        ctx.context.research = {}
    ctx.context.research[topic] = findings
    return f"Research saved for topic: {topic} ({len(findings)} chars)"


@function_tool
def get_all_research(ctx: RunContextWrapper) -> str:
    """Retrieve all saved research findings from context."""
    if not hasattr(ctx.context, "research") or not ctx.context.research:
        return "No research has been saved yet."

    sections = []
    for topic, findings in ctx.context.research.items():
        sections.append(f"## {topic}\n{findings}")
    return "\n\n".join(sections)


@function_tool
def save_draft(ctx: RunContextWrapper, content: str) -> str:
    """Save a draft article to shared context.

    Args:
        content: The full draft content.
    """
    ctx.context.draft = content
    ctx.context.draft_version = getattr(ctx.context, "draft_version", 0) + 1
    return f"Draft v{ctx.context.draft_version} saved ({len(content)} chars)"


@function_tool
def get_draft(ctx: RunContextWrapper) -> str:
    """Retrieve the current draft from context."""
    draft = getattr(ctx.context, "draft", None)
    if not draft:
        return "No draft has been written yet."
    version = getattr(ctx.context, "draft_version", "?")
    return f"[Draft v{version}]\n\n{draft}"
