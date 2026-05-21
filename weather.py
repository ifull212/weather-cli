#!/usr/bin/env python3
"""CLI weather tool — get current weather for any city."""
import argparse
import json
import sys
import urllib.request

API_KEY = "demo"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str, units: str = "metric") -> dict:
    url = f"{BASE_URL}?q={city}&units={units}&appid={API_KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "weather-cli/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def format_weather(data: dict) -> str:
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    lines = [
        f"Weather in {city}, {country}",
        f"  Temperature: {temp}°C (feels like {feels}°C)",
        f"  Condition: {desc}",
        f"  Humidity: {humidity}%",
        f"  Wind: {wind} m/s",
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Get weather for a city")
    parser.add_argument("city", help="City name")
    parser.add_argument("--imperial", action="store_true", help="Use Fahrenheit")
    args = parser.parse_args()

    units = "imperial" if args.imperial else "metric"
    try:
        data = get_weather(args.city, units)
        print(format_weather(data))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
