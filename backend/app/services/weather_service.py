import httpx
from typing import Optional


OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

# Venue coordinates (sample venues — can be extended)
VENUE_COORDS = {
    "Old Trafford": {"lat": 53.4631, "lon": -2.2913},
    "Camp Nou": {"lat": 41.3809, "lon": 2.1228},
    "Wembley Stadium": {"lat": 51.5560, "lon": -0.2796},
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Wimbledon": {"lat": 51.4340, "lon": -0.2143},
    "default": {"lat": 51.5074, "lon": -0.1278},  # London default
}


async def get_weather_for_venue(venue: Optional[str]) -> Optional[str]:
    """
    Fetch real-time weather from Open-Meteo (free, no API key).
    Returns a human-readable weather string for injection into Gemini prompt.
    """
    try:
        coords = VENUE_COORDS.get(venue, VENUE_COORDS["default"]) if venue else VENUE_COORDS["default"]

        async with httpx.AsyncClient(timeout=5.0) as client:
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,weather_code,wind_speed_10m,precipitation",
                "wind_speed_unit": "kmh",
            }
            resp = await client.get(OPEN_METEO_BASE, params=params)
            if resp.status_code != 200:
                return None

            data = resp.json()
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            wind = current.get("wind_speed_10m")
            rain = current.get("precipitation", 0)
            code = current.get("weather_code", 0)

            condition = _weather_code_to_text(code, rain)
            return f"{temp}°C, {condition}, Wind: {wind} km/h"
    except Exception as e:
        print(f"[Weather] Error fetching weather: {e}")
        return None


def _weather_code_to_text(code: int, precipitation: float) -> str:
    """Convert WMO weather code to human-readable text."""
    if code == 0:
        return "Clear sky"
    elif code <= 3:
        return "Partly cloudy"
    elif code <= 9:
        return "Fog"
    elif code <= 29:
        return "Drizzle"
    elif code <= 39:
        return "Rain"
    elif precipitation > 5:
        return "Heavy rain"
    elif precipitation > 0:
        return "Light rain"
    elif code <= 59:
        return "Overcast"
    elif code <= 69:
        return "Snow"
    elif code <= 79:
        return "Sleet"
    elif code <= 99:
        return "Thunderstorm"
    return "Variable conditions"
