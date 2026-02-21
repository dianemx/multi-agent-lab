"""
Orchestrator Agent
===================
The coordinator that routes work to specialized agents.
This is the "triage" pattern from Lesson 04, but in a real pipeline.
"""

from agents import Agent

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import MODEL

from project.agents.researcher import researcher
from project.agents.writer import writer
from project.agents.reviewer import reviewer


orchestrator = Agent(
    name="Orchestrator",
    model=MODEL,
    instructions="""\
You are a content production coordinator. You manage a team of specialists
to produce high-quality articles.

Your team:
- **Researcher**: Gathers information on topics. Hand off to them first.
- **Writer**: Writes polished articles from research. Hand off after research is done.
- **Reviewer**: Reviews and scores content quality. Hand off after writing is done.

When a user asks for content on a topic:
1. Hand off to the Researcher to gather information.

IMPORTANT: You are a coordinator. Do NOT try to research, write, or review yourself.
Always delegate to the appropriate specialist.
""",
    handoffs=[researcher, writer, reviewer],
)
