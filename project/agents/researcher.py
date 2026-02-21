"""
Researcher Agent
=================
Gathers and synthesizes information on a topic using search tools.
Stores findings in the shared context for other agents to use.
"""

from agents import Agent

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import MODEL

from project.tools.web_search import web_search, web_search_detailed
from project.tools.file_tools import save_research, get_all_research


researcher = Agent(
    name="Researcher",
    model=MODEL,
    instructions="""\
You are an expert research analyst. Your job is to gather comprehensive
information on a given topic.

Your workflow:
1. Break the topic into 2-3 key subtopics to research.
2. Use web_search for each subtopic.
3. Synthesize the findings into clear, well-organized research notes.
4. Save your findings using save_research (one save per subtopic).

Guidelines:
- Be thorough but concise — focus on facts, data, and key insights.
- Note any conflicting information or gaps.
- Always cite the source titles in your notes.
- When done, summarize what you found and what subtopics you covered.
""",
    tools=[web_search, web_search_detailed, save_research, get_all_research],
    handoff_description="Specialist that researches topics and gathers information",
)
