# Weather Illustration Generator - Workshop Exercises

## Base Project

The script already:
- Converts a city name to coordinates (Open-Meteo Geocoding API)
- Fetches current weather (Open-Meteo Forecast API)
- Builds an image prompt with city + weather context
- Generates an isometric 3D illustration via Gemini API

Run it: `python weather.py "Mainz"`

---

## Exercise 1: Multiple Styles via CLI Flag

**Goal:** Add a `--style` flag so users can choose different illustration styles.

**Steps:**

1. Replace `sys.argv` parsing with `argparse`:
```python
import argparse

parser = argparse.ArgumentParser(description="Weather Illustration Generator")
parser.add_argument("city", help="City name to generate weather illustration for")
parser.add_argument("--style", choices=["isometric", "ghibli", "pixel", "cyberpunk"], default="isometric")
args = parser.parse_args()
```

2. Create a `STYLES` dictionary with prompt templates per style:
```python
STYLES = {
    "isometric": "Present a clear, 45° top-down view of a horizontal (16:9) landscape isometric miniature 3D cartoon scene...",
    "ghibli": "A Studio Ghibli-style illustration, soft dreamy lighting, painterly watercolor backgrounds, Hayao Miyazaki inspired...",
    "pixel": "A detailed isometric pixel art scene, retro game aesthetic, 16-bit color palette...",
    "cyberpunk": "A moody cyberpunk cityscape at night, neon-lit signs, rain-soaked streets, high contrast...",
}
```

3. Modify `build_prompt()` to accept a `style` parameter and use the matching template.

**Hints:**
- Each style template should still include `{city}`, `{condition}`, `{temp}` placeholders
- Keep the "no extra text" rule across all styles
- Test with: `python weather.py "Tokyo" --style cyberpunk`

---

## Exercise 2: 3-Day Forecast Mode

**Goal:** Add a `--forecast` flag that generates illustrations for today + next 2 days.

**Steps:**

1. Add a new API call to fetch the daily forecast. Open-Meteo supports this:
```python
params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": "weathercode,temperature_2m_max,temperature_2m_min",
    "timezone": "auto",
    "forecast_days": 3,
}
```
The response contains `daily.weathercode`, `daily.temperature_2m_max`, `daily.temperature_2m_min`, and `daily.time` as arrays.

2. Create a `get_forecast()` function that returns a list of daily weather dicts:
```python
def get_forecast(latitude: float, longitude: float, days: int = 3) -> list[dict]:
    # Returns: [{"date": "2026-06-08", "condition": "overcast", "temp_max": 22.1, "temp_min": 14.3}, ...]
```

3. Loop through forecast days, build a prompt for each, and generate images:
```python
for i, day in enumerate(forecast):
    prompt = build_prompt(city, country, day)
    filepath = generate_image(prompt, output_dir)
    print(f"  Day {i+1}: {filepath}")
```

**Hints:**
- Modify `build_prompt()` to accept a date string instead of always using `datetime.now()`
- Show temp range (min/max) instead of single temperature for forecast days
- Name output files with the date: `weather_mainz_2026-06-08.png`
- Test with: `python weather.py "Berlin" --forecast`

---

## Exercise 3: Sunrise/Sunset Lighting

**Goal:** Adapt the scene lighting in the prompt based on actual sunrise/sunset times.

**Steps:**

1. Add sunrise/sunset to the weather API call:
```python
params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True,
    "daily": "sunrise,sunset",
    "timezone": "auto",
}
```
Response includes `daily.sunrise[0]` and `daily.sunset[0]` as ISO timestamps.

2. Create a `get_lighting_mood()` function:
```python
def get_lighting_mood(current_time: datetime, sunrise: str, sunset: str) -> str:
    """Determine lighting based on actual sun position."""
    # Parse sunrise/sunset times
    # Compare current time to determine:
    # - Before sunrise: "pre-dawn blue hour, deep indigo sky"
    # - Around sunrise (±30min): "golden sunrise, warm orange horizon"
    # - Morning: "bright clear morning light"
    # - Midday: "high noon, strong overhead sun, short shadows"
    # - Around sunset (±30min): "golden hour, long amber shadows"
    # - After sunset: "twilight dusk, purple and pink sky"
    # - Night: "moonlit night scene, soft blue tones, warm window light"
```

3. Inject the lighting mood into the prompt:
```python
prompt = (
    f"... The lighting is {lighting_mood}. ..."
)
```

**Hints:**
- Use `datetime.fromisoformat()` to parse the sunrise/sunset strings
- The Open-Meteo API returns times in the location's timezone (when you set `timezone=auto`)
- Consider the weather condition too: overcast skies diffuse light differently than clear skies
- Test by temporarily overriding the hour to see different moods

---

## Bonus Ideas (if time permits)

- **Error handling:** What happens if the Gemini API rate-limits you? Add retry logic with `time.sleep()`.
- **Image viewer:** Auto-open the generated image with `subprocess.run(["open", filepath])` on macOS.
- **Config file:** Move styles/settings to a `config.json` so non-coders can tweak prompts.
