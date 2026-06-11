"""
Weather Illustration Generator
Fetches current weather for a city and generates a Studio Ghibli-style illustration.

Usage: python weather.py "City Name"
"""

import sys
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# --- Weather Code Descriptions ---

WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snowfall",
    73: "moderate snowfall",
    75: "heavy snowfall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


def geocode_city(city_name: str) -> dict:
    """Convert city name to coordinates using Open-Meteo Geocoding API."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"City '{city_name}' not found.")

    result = data["results"][0]
    return {
        "name": result["name"],
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
    }


def get_weather(latitude: float, longitude: float) -> dict:
    """Fetch current weather from Open-Meteo Forecast API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    current = data["current_weather"]

    weather_code = current["weathercode"]
    return {
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "winddirection": current["winddirection"],
        "weather_code": weather_code,
        "condition": WEATHER_CODES.get(weather_code, "unknown"),
    }


def build_prompt(city: str, country: str, weather: dict) -> str:
    """Build an isometric 3D miniature weather scene prompt."""
    condition = weather["condition"]

    prompt = (
        f"Present a clear, 45° top-down view of a horizontal (16:9) landscape isometric miniature 3D cartoon scene, "
        f"showcasing a wide panoramic view of {city}, {country} with as many iconic landmarks, famous buildings, "
        f"and recognizable architecture as possible, all centered in the composition to showcase precise and delicate modeling. "
        f"Include multiple well-known landmarks spread across the scene to create a rich, detailed cityscape. "
        f"Fill the scene with architectural details: bridges, towers, churches, historic buildings, parks, and rivers "
        f"that are characteristic of {city}.\n\n"
        f"The scene features soft, refined textures with realistic PBR materials and gentle, lifelike "
        f"lighting and shadow effects. The current weather is {condition}. "
        f"Weather elements are creatively integrated into the urban architecture, establishing a dynamic "
        f"interaction between the city's landscape and atmospheric conditions, creating an immersive "
        f"weather ambiance.\n\n"
        f"Use a clean, unified composition with minimalistic aesthetics and a soft, solid-colored "
        f"background that highlights the main content. The overall visual style is fresh and soothing.\n\n"
        f"Display a prominent weather icon at the top-center representing {condition}. "
        f"The weather icon has no background and can subtly overlap with the buildings.\n\n"
        f"STRICT: Do NOT include ANY text, numbers, letters, street names, landmark labels, signs, "
        f"descriptions, banners, dates, or temperature readings anywhere in the image."
    )
    return prompt


def generate_image(prompt: str, output_dir: str) -> str:
    """Generate an image using Gemini's native image generation."""
    os.makedirs(output_dir, exist_ok=True)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.1-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    # Extract the image from the response
    if not response.candidates:
        raise RuntimeError("No response from Gemini API.")

    content = response.candidates[0].content
    if not content or not content.parts:
        raise RuntimeError("No content in Gemini response.")

    for part in content.parts:
        if part.inline_data is not None and part.inline_data.data:
            image_data = part.inline_data.data

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weather_illustration_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(image_data)

            return filepath

    raise RuntimeError("No image returned from Gemini API.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python weather.py \"City Name\"")
        sys.exit(1)

    city_input = sys.argv[1]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

    # 1. Geocode
    print(f"Geocoding '{city_input}'...")
    location = geocode_city(city_input)
    print(f"  Found: {location['name']}, {location['country']}")
    print(f"  Coordinates: {location['latitude']}, {location['longitude']}")

    # 2. Fetch weather
    print(f"\nFetching weather...")
    weather = get_weather(location["latitude"], location["longitude"])
    print(f"  Condition: {weather['condition']}")
    print(f"  Temperature: {weather['temperature']}°C")
    print(f"  Wind Speed: {weather['windspeed']} km/h")

    # 3. Build prompt
    prompt = build_prompt(location["name"], location["country"], weather)
    print(f"\nGenerated prompt:")
    print(f"  {prompt}")

    # 4. Generate image
    print(f"\nGenerating isometric weather illustration...")
    filepath = generate_image(prompt, output_dir)
    print(f"  Saved to: {filepath}")


if __name__ == "__main__":
    main()
