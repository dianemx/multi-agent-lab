"""
Shared configuration for the Multi-Agent Lab.
All lessons import from here so you configure Azure OpenAI once.

This uses the Chat Completions API path, which is widely supported
across all Azure OpenAI deployments and API versions.
"""

import os
import sys

from dotenv import load_dotenv

# Load .env from project root (works from any lesson subfolder)
_root = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_root, ".env"))

# Suppress "OPENAI_API_KEY is not set, skipping trace export" warning.
# We're using Azure, not a direct OpenAI key.
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "unused"

from openai import AsyncAzureOpenAI
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents import set_tracing_disabled

# Disable tracing export to OpenAI (we're using Azure, not an OpenAI API key).
# Re-enable this if you set up a custom tracing backend.
set_tracing_disabled(True)

# ── Azure OpenAI settings ───────────────────────────────────────────
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-03-01-preview")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
    print("ERROR: Missing Azure OpenAI configuration.")
    print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in your .env file.")
    print("See .env.example for details.")
    sys.exit(1)

# ── Create the Azure OpenAI async client ─────────────────────────────
_client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# ── Model wrapper for the Agents SDK ─────────────────────────────────
# This wraps the Azure client so the Agents SDK can use it.
# Pass MODEL to any Agent(model=MODEL, ...) definition.
MODEL = OpenAIChatCompletionsModel(
    model=AZURE_OPENAI_DEPLOYMENT,
    openai_client=_client,
)


def get_model(deployment: str | None = None) -> OpenAIChatCompletionsModel:
    """Get a model instance, optionally for a different deployment.

    Args:
        deployment: Azure deployment name. Defaults to AZURE_OPENAI_DEPLOYMENT.
    """
    if deployment is None or deployment == AZURE_OPENAI_DEPLOYMENT:
        return MODEL
    return OpenAIChatCompletionsModel(
        model=deployment,
        openai_client=_client,
    )
