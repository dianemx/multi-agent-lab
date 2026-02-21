"""
Lesson 02 — Tools
==================
Agents become powerful when they can DO things.
Tools are plain Python functions that the agent can choose to call.

Key takeaways:
  • Decorate a function with @function_tool to make it available to an agent.
  • The function's docstring and type hints tell the LLM what the tool does.
  • The agent decides WHEN and WHETHER to call each tool.
  • The Runner executes the function and feeds the result back to the LLM.
"""

import asyncio
import os
import sys
import random
from datetime import datetime

# Add project root to path so we can import the shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from config import MODEL
from agents import Agent, Runner, function_tool
import json


# ── Define tools ─────────────────────────────────────────────────────
# A tool is just a Python function with a docstring and type hints.
# The @function_tool decorator registers it so the agent can use it.


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.

    Args:
        city: The name of the city to check weather for.
    """
    # In a real app, you'd call a weather API here.
    # For learning, we'll return mock data.

    # Try to fetch real weather data from Open-Meteo (free, no API key needed)
    try:
        import urllib.request
        import urllib.parse
        import ssl
        import certifi

        # Create SSL context using certifi's certificate bundle
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())

        # Step 1: Geocode the city name to lat/lon using Open-Meteo's geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        with urllib.request.urlopen(geo_url, timeout=5, context=ssl_ctx) as geo_response:
            geo_data = json.loads(geo_response.read().decode())

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            return f"Sorry, I couldn't find a city named '{city}'."

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        resolved_name = geo_data["results"][0].get("name", city)
        country = geo_data["results"][0].get("country", "")

        # Step 2: Fetch current weather from Open-Meteo
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )
        with urllib.request.urlopen(weather_url, timeout=5, context=ssl_ctx) as weather_response:
            weather_data = json.loads(weather_response.read().decode())

        cw = weather_data["current_weather"]
        temp = cw["temperature"]
        windspeed = cw["windspeed"]
        # Map WMO weather codes to human-readable descriptions
        wmo_codes = {
            0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
            45: "foggy", 48: "depositing rime fog",
            51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
            61: "slight rain", 63: "moderate rain", 65: "heavy rain",
            71: "slight snowfall", 73: "moderate snowfall", 75: "heavy snowfall",
            77: "snow grains", 80: "slight rain showers", 81: "moderate rain showers",
            82: "violent rain showers", 85: "slight snow showers", 86: "heavy snow showers",
            95: "thunderstorm", 96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail",
        }
        condition = wmo_codes.get(cw.get("weathercode"), "unknown")

        return (
            f"Weather in {resolved_name} ({country}): {temp}°C, {condition}, "
            f"wind {windspeed} km/h"
        )
    except Exception as e:
        print(f"Weather API error for {city}: {type(e).__name__}: {e}")
        pass  # Fall back to mock data below

    conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    temp = random.randint(-5, 35)
    condition = random.choice(conditions)
    return f"Weather in {city}: {temp}°C, {condition}"


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result.

    Args:
        expression: A math expression like '2 + 2' or '(10 * 5) / 3'.
    """
    try:
        # WARNING: eval() is dangerous in production! This is just for learning.
        # In a real app, use a safe math parser.
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@function_tool
def get_current_date() -> str:
    """Get today's date and day of the week."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y — %H:%M")


# -- getTime() function --

@function_tool
def get_time() -> str:
    """Get the current time."""
    now = datetime.now()
    return now.strftime("%H:%M:%S")

# -- convertCurrency(amount, fromCurrency, toCurrency) function --
@function_tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another.

    Args:
        amount: The amount of money to convert.
        from_currency: The currency code to convert from (e.g., 'USD').
        to_currency: The currency code to convert to (e.g., 'EUR').
    """
   
    # Try to fetch real exchange rates from a free API
    try:
        import urllib.request
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("result") == "success":
                rate = data["rates"].get(to_currency.upper())
                if rate is not None:
                    converted_amount = amount * rate
                    return f"{amount} {from_currency.upper()} is approximately {converted_amount:.2f} {to_currency.upper()}."
    except Exception as e:
        print(f"Currency API error: {type(e).__name__}: {e}")
        pass  # Fall back to mock exchange rates below

    # Fallback: mock exchange rates if the API is unavailable
    exchange_rates = {
        ("USD", "EUR"): 0.85,
        ("EUR", "USD"): 1.18,
        ("USD", "JPY"): 110.0,
        ("JPY", "USD"): 0.0091,
        ("EUR", "JPY"): 129.53,
        ("JPY", "EUR"): 0.0077,
    }
    rate = exchange_rates.get((from_currency.upper(), to_currency.upper()))
    if rate is None:
        return f"Sorry, I don't have the exchange rate for {from_currency} to {to_currency}."
    converted_amount = amount * rate
    return f"{amount} {from_currency.upper()} is approximately {converted_amount:.2f} {to_currency.upper()}."

# ── Define the agent with tools ─────────────────────────────────────
agent = Agent(
    name="Tool-Equipped Assistant",
    instructions=(
        "You are a helpful assistant with access to tools. "
        "Use the available tools when the user's question requires them. "
        "Always report tool results clearly."
    ),
    model=MODEL,
    tools=[get_weather, calculate, get_current_date, get_time, convert_currency],
)


# ── Run ──────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  LESSON 02 — Tools")
    print("=" * 60)

    # This question should trigger the weather tool
    questions = [
        "What's the weather like in Rome and Tokyo today?",
        "What is 42 * 17 + 3?",
        "What day is it today, and what's the weather in Milan?",
        "What time is it now?",
        "Convert 100 USD to EUR.",
        "Convert 50 EUR to JPY and perform 3+3",
        "Tell me date and time",
    ]

    for q in questions:
        print(f"\n🧑 You: {q}")
        result = await Runner.run(agent, q)
        print(f"🤖 Agent: {result.final_output}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())
