"""
Writer Agent
=============
Creates polished content from research findings.
Reads research from context and produces a well-structured draft.
"""

from agents import Agent

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import MODEL

from project.tools.file_tools import get_all_research, save_draft, get_draft


writer = Agent(
    name="Writer",
    model=MODEL,
    instructions="""\
You are an expert content writer. Your job is to create engaging,
well-structured articles from research notes.

Your workflow:
1. Use get_all_research to retrieve the research findings.
2. Organize the information into a compelling narrative.
3. Write the full article.
4. Save the draft using save_draft.

Writing guidelines:
- Start with a hook that draws the reader in.
- Use clear section headers (##).
- Balance depth with readability — write for an educated general audience.
- Include specific data points and examples from the research.
- End with a forward-looking conclusion.
- Target length: 400-600 words.
""",
    tools=[get_all_research, save_draft, get_draft],
    handoff_description="Specialist that writes polished content from research",
)
