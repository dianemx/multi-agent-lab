"""
Simulated web search tool.

In a real project, you'd replace this with:
  - Tavily API (tavily.com) — built for AI agents
  - Brave Search API
  - SerpAPI / Google Custom Search
  - Or httpx calls to any search API
"""

from agents import function_tool, RunContextWrapper

# ── Simulated search database ───────────────────────────────────────
# Enough content to make the demos realistic and educational.

SEARCH_DATA = {
    "quantum computing": [
        {
            "title": "What is Quantum Computing? — IBM",
            "snippet": (
                "Quantum computing uses quantum bits (qubits) that can exist in superposition, "
                "representing both 0 and 1 simultaneously. This enables quantum computers to "
                "solve certain problems exponentially faster than classical computers."
            ),
        },
        {
            "title": "Quantum Computing Applications — Nature",
            "snippet": (
                "Key applications include drug discovery, cryptography, optimization problems, "
                "financial modeling, and materials science. Google's Sycamore achieved quantum "
                "supremacy in 2019, solving a problem in 200 seconds that would take a "
                "classical supercomputer 10,000 years."
            ),
        },
        {
            "title": "Challenges in Quantum Computing — MIT Technology Review",
            "snippet": (
                "Major challenges include qubit decoherence, error correction, and the need for "
                "extremely low temperatures (near absolute zero). Current quantum computers have "
                "50-1000+ qubits, but millions may be needed for practical applications."
            ),
        },
    ],
    "renewable energy": [
        {
            "title": "State of Renewable Energy 2025 — IEA",
            "snippet": (
                "Renewable energy accounted for 30% of global electricity generation in 2024. "
                "Solar and wind are now the cheapest sources of new electricity in most countries. "
                "Global investment in clean energy reached $1.8 trillion in 2024."
            ),
        },
        {
            "title": "Future of Energy Storage — Bloomberg NEF",
            "snippet": (
                "Battery storage costs have fallen 90% since 2010. Grid-scale storage is essential "
                "for renewable reliability. New technologies like solid-state batteries and green "
                "hydrogen are emerging as game-changers."
            ),
        },
        {
            "title": "Renewable Energy Challenges — World Economic Forum",
            "snippet": (
                "Key challenges include grid infrastructure, intermittency, supply chain for "
                "critical minerals, and political/regulatory barriers. However, the economic case "
                "for renewables continues to strengthen."
            ),
        },
    ],
    "artificial intelligence": [
        {
            "title": "The State of AI — Stanford HAI Report",
            "snippet": (
                "AI systems now match or exceed human performance in image classification, "
                "language understanding, and code generation. Foundation models (LLMs) are "
                "being applied across every industry."
            ),
        },
        {
            "title": "AI Agents — OpenAI Research",
            "snippet": (
                "Agentic AI systems can autonomously plan, use tools, and complete multi-step "
                "tasks. Multi-agent systems enable collaboration between specialized AI agents, "
                "mimicking how human teams work."
            ),
        },
        {
            "title": "AI Risks and Governance — OECD",
            "snippet": (
                "Key concerns include bias, misinformation, job displacement, and autonomous "
                "weapons. Over 60 countries have published AI governance frameworks. "
                "The EU AI Act is the most comprehensive regulation to date."
            ),
        },
    ],
}


@function_tool
def web_search(query: str) -> str:
    """Search the web for information on a topic.

    Args:
        query: The search query string.
    """
    # Find the best matching topic
    query_lower = query.lower()
    for topic, results in SEARCH_DATA.items():
        if topic in query_lower or any(word in query_lower for word in topic.split()):
            formatted = []
            for r in results:
                formatted.append(f"**{r['title']}**\n{r['snippet']}")
            return "\n\n".join(formatted)

    # Fallback: return generic results
    return (
        f"Search results for '{query}':\n"
        "No specific results found. The topic appears to be niche. "
        "Consider breaking it down into more specific sub-queries."
    )


@function_tool
def web_search_detailed(query: str, num_results: int) -> str:
    """Search the web with a specified number of results.

    Args:
        query: The search query string.
        num_results: Maximum number of results to return (1-5).
    """
    query_lower = query.lower()
    for topic, results in SEARCH_DATA.items():
        if topic in query_lower or any(word in query_lower for word in topic.split()):
            limited = results[:num_results]
            formatted = []
            for i, r in enumerate(limited, 1):
                formatted.append(f"{i}. **{r['title']}**\n   {r['snippet']}")
            return "\n\n".join(formatted)

    return f"No results found for '{query}'"
