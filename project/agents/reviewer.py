"""
Reviewer Agent
===============
Reviews content quality and provides structured feedback.
Uses structured output to ensure consistent, actionable reviews.
"""

from pydantic import BaseModel, Field
from agents import Agent

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import MODEL

from project.tools.file_tools import get_draft


class ContentReview(BaseModel):
    """Structured review of a piece of content."""

    overall_score: float = Field(
        description="Overall quality score from 1-10",
        ge=1,
        le=10,
    )
    strengths: list[str] = Field(
        description="List of strengths in the content (2-4 items)",
    )
    weaknesses: list[str] = Field(
        description="List of areas for improvement (2-4 items)",
    )
    suggestions: list[str] = Field(
        description="Specific, actionable suggestions for improvement",
    )
    verdict: str = Field(
        description="One of: publish, needs_revision, major_rewrite",
    )
    summary: str = Field(
        description="2-3 sentence summary of the review",
    )


reviewer = Agent(
    name="Reviewer",
    model=MODEL,
    instructions="""\
You are a senior content editor and quality reviewer. Your job is to
critically evaluate written content and provide structured feedback.

Your workflow:
1. Use get_draft to read the current draft.
2. Evaluate it thoroughly.
3. Return your structured review.

Evaluation criteria:
- **Accuracy**: Are claims supported by facts? Any errors?
- **Structure**: Is it well-organized with clear sections?
- **Engagement**: Is it interesting to read? Good hook?
- **Completeness**: Does it cover the topic adequately?
- **Clarity**: Is the writing clear and accessible?

Scoring guide:
- 9-10: Excellent, ready to publish
- 7-8: Good, minor improvements needed
- 5-6: Adequate, needs significant revision
- 1-4: Poor, needs major rewrite

Be constructive but honest. Give specific, actionable feedback.
""",
    tools=[get_draft],
    output_type=ContentReview,
    handoff_description="Specialist that reviews and critiques written content",
)
