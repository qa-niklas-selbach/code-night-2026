# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt        # install deps
python weather.py "Berlin"             # run: geocode → fetch weather → generate image
```

Requires `GEMINI_API_KEY` in `.env` (loaded via `python-dotenv`). No tests, no lint config.

## Architecture

Single-file CLI (`weather.py`) that runs a fixed 4-step pipeline in `main()`:

1. **`geocode_city`** → Open-Meteo Geocoding API (no key) resolves a city name to lat/lon + country.
2. **`get_weather`** → Open-Meteo Forecast API returns `current_weather`; numeric `weathercode` is mapped to a human-readable condition via the `WEATHER_CODES` dict.
3. **`build_prompt`** → assembles a long, hardcoded English prompt for an isometric 3D miniature cityscape. The prompt embeds the city, country, condition, temperature, and today's date (formatted with German locale `de_DE.UTF-8`, falling back silently if unavailable). It instructs the model to render text overlays (city name, date, temperature) **in German** and forbids any other text in the image.
4. **`generate_image`** → calls `google.genai` with model `gemini-3.1-flash-image` and `response_modalities=["TEXT", "IMAGE"]`. Walks `response.candidates[0].content.parts` for the first `inline_data` payload and writes it as `output/weather_illustration_<YYYYMMDD_HHMMSS>.png`.

Notes for edits:
- Weather data is sourced from `current_weather` only; hourly/daily fields aren't fetched.
- `WEATHER_CODES` is the single source of truth for condition strings used in the prompt — extend this dict rather than hardcoding conditions elsewhere.
- The Gemini model ID and response-parsing loop are tightly coupled to the current `google-genai` SDK shape; changing the model may require adjusting how `inline_data` is extracted.