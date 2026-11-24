
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def find_city(city):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=10
    )
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        return None

    result = results[0]

    return {
        "name": result["name"],
        "country": result.get("country", "Unknown"),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset"
        ],
        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    return descriptions.get(code, "Unknown weather condition")
