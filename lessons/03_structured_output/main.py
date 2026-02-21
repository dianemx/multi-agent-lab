"""
Lesson 03 — Structured Output
===============================
Instead of free-form text, make agents return validated Pydantic objects.

Key takeaways:
  • Set output_type=YourModel on an Agent to enforce structured output.
  • The LLM generates JSON matching the schema; the SDK validates it.
  • result.final_output is a Pydantic model instance — access fields directly.
  • This is how you connect agents in a pipeline (output of one → input of next).
"""

import asyncio
import os
import sys

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from pydantic import BaseModel, Field
from agents import Agent, Runner


# ── Define output schemas as Pydantic models ────────────────────────
class MovieRecommendation(BaseModel):
    """A structured movie recommendation."""

    title: str = Field(description="The movie title")
    genre: str = Field(description="Primary genre")
    why: str = Field(description="Why the user would enjoy this movie (2-3 sentences)")
    rating: float = Field(description="IMDb-style rating out of 10", ge=0, le=10)
    director: str = Field(description="The director of the movie")
    year: int = Field(description="The release year of the movie")
    main_actors: list[str] = Field(description="List of main actors in the movie")


class SentimentAnalysis(BaseModel):
    """Structured sentiment analysis of a text."""

    sentiment: str = Field(description="One of: positive, negative, neutral, mixed")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0", ge=0, le=1)
    key_phrases: list[str] = Field(description="Key phrases that influenced the analysis")
    summary: str = Field(description="One-sentence summary of the sentiment")

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

class AllMovies(BaseModel):
    """Structured output for multiple movie recommendations."""

    movies: list[MovieRecommendation] = Field(description="List of movie recommendations")  

# ── Agents with structured output ───────────────────────────────────
movie_agent = Agent(
    name="Movie Recommender",
    instructions=(
        "You are a movie expert. Given a user's mood or preference, "
        "recommend ONE perfect movie. Be specific about why it fits."
    ),
    model=MODEL,
    output_type=MovieRecommendation,  # ← This is the magic
)

sentiment_agent = Agent(
    name="Sentiment Analyzer",
    instructions=(
        "You analyze the sentiment of text. "
        "Be precise and identify the key phrases driving the sentiment."
    ),
    model=MODEL,
    output_type=SentimentAnalysis,
)

content_review_agent = Agent(
    name="Content Reviewer",
    instructions=(
        "You review a piece of content and provide a structured assessment. "
        "Be specific and actionable in your feedback."
    ),
    model=MODEL,
    output_type=ContentReview,
)

multiple_movies_agent = Agent(
    name="Multiple Movie Recommender",
    instructions=(
        "You are a movie expert. Given a user's mood or preference, "
        "recommend THREE perfect movies. Be specific about why each fits."
    ),
    model=MODEL,
    output_type=AllMovies,  # ← This agent returns multiple movie recommendations in a structured format
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 03 — Structured Output")
    print("=" * 60)

    # ── Example 1: Movie recommendation ──────────────────────────────
    print("\n📽️  Movie Recommendation Agent")
    print("-" * 40)

    result = await Runner.run(
        movie_agent,
        "I'm feeling nostalgic and want something sci-fi from the 80s or 90s",
    )

    # result.final_output is a MovieRecommendation instance!
    movie = result.final_output
    print(f"  Title:  {movie.title}")
    print(f"  Genre:  {movie.genre}")
    print(f"  Rating: {movie.rating}/10")
    print(f"  Director: {movie.director}")
    print(f"  Year: {movie.year}")
    print(f"  Main Actors: {', '.join(movie.main_actors)}")
    print(f"  Why:    {movie.why}")

    # ── Example 2: Sentiment analysis ────────────────────────────────
    # print("\n🔍 Sentiment Analysis Agent")
    # print("-" * 40)

    # text = (
    #     "The new update is mostly great — the UI is much cleaner and faster. "
    #     "However, the removal of the export feature is really frustrating "
    #     "and breaks my workflow."
    # )
    # print(f"  Text: {text}\n")

    # result = await Runner.run(sentiment_agent, text)

    # sentiment = result.final_output
    # print(f"  Sentiment:   {sentiment.sentiment}")
    # print(f"  Confidence:  {sentiment.confidence:.0%}")
    # print(f"  Key phrases: {', '.join(sentiment.key_phrases)}")
    # print(f"  Summary:     {sentiment.summary}")

    # ── Example 3: Chaining — output of one feeds into another ───────
    print("\n🔗 Chaining: Movie → Sentiment")
    print("-" * 40)

    movie_result = await Runner.run(
        movie_agent, "Something dark and thought-provoking"
    )
    movie = movie_result.final_output

    # Use the movie recommendation as input to sentiment analysis
    sentiment_result = await Runner.run(
        sentiment_agent,
        f"Analyze the sentiment of this review: '{movie.why}'",
    )
    sentiment = sentiment_result.final_output

    print(f"  Movie: {movie.title}")
    print(f"  Review: {movie.why}")
    print(f"  Review sentiment: {sentiment.sentiment} ({sentiment.confidence:.0%})")
    print(f"  Key phrases: {', '.join(sentiment.key_phrases)}")
    print(f"  Summary: {sentiment.summary}")

    # ── Example 4: Content Review of Movie Recommendation ───────────
    print("\n📝 Content Review Agent")
    print("-" * 40)

    print(f"  Reviewing the movie recommendation for: {movie.title}")
    print(f"  Content: {movie.why}\n")

    result = await Runner.run(
        content_review_agent,
        f"Review the following movie recommendation text:\n\n'{movie.why}'",
    )

    review = result.final_output
    print(f"  Overall Score: {review.overall_score}/10")
    print(f"  Verdict:       {review.verdict}")
    print(f"  Summary:       {review.summary}")
    print(f"  Strengths:")
    for s in review.strengths:
        print(f"    ✅ {s}")
    print(f"  Weaknesses:")
    for w in review.weaknesses:
        print(f"    ❌ {w}")
    print(f"  Suggestions:")
    for s in review.suggestions:
        print(f"    💡 {s}")

    # ── Example 5: Multiple Movie Recommendations ───────────────────
    print("\n🎬 Multiple Movie Recommendations Agent")
    print("-" * 40)

    result = await Runner.run(
        multiple_movies_agent,
        "I love mind-bending thrillers with unexpected twists",
    )

    all_movies = result.final_output
    for i, movie in enumerate(all_movies.movies, 1):
        print(f"\n  🎥 Movie {i}:")
        print(f"    Title:    {movie.title}")
        print(f"    Genre:    {movie.genre}")
        print(f"    Rating:   {movie.rating}/10")
        print(f"    Director: {movie.director}")
        print(f"    Year:     {movie.year}")
        print(f"    Actors:   {', '.join(movie.main_actors)}")
        print(f"    Why:      {movie.why}")

if __name__ == "__main__":
    asyncio.run(main())
