import requests
from datetime import date


# =========================================
# GET COORDINATES
# =========================================

def get_coordinates(location, country_code="IN"):

    location = location.strip()

    geo_url = (
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={location}&count=10&language=en&format=json"
    )

    try:
        response = requests.get(geo_url, timeout=10)
        data = response.json()

    except requests.exceptions.RequestException as e:
        print("Network/API Error:", e)
        return None, None

    if "results" not in data or len(data["results"]) == 0:
        print("Location not found!")
        return None, None

    # Filter results by country code
    matched = [
        r for r in data["results"]
        if r.get("country_code", "").upper() == country_code.upper()
    ]

    if not matched:
        print(f"No results found in country code '{country_code}'.")
        print("Available matches found in other countries:")
        for r in data["results"]:
            print(f"  - {r.get('name')}, {r.get('admin1')}, {r.get('country')} ({r.get('country_code')})")
        return None, None

    result = matched[0]
    latitude  = result["latitude"]
    longitude = result["longitude"]
    print(f"Location found: {result.get('name')}, {result.get('admin1')}, {result.get('country')}")
    print(f"Coordinates: {latitude}, {longitude}")

    return latitude, longitude


# =========================================
# GET LIVE WEATHER
# =========================================

def get_weather_data(location, country_code="IN"):

    latitude, longitude = get_coordinates(location, country_code)

    if latitude is None:
        return None

    today = date.today().isoformat()

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,relativehumidity_2m,surface_pressure,windspeed_10m"
        f"&daily=temperature_2m_min,temperature_2m_max,precipitation_sum"
        f"&timezone=Asia/Kolkata"
        f"&start_date={today}&end_date={today}"
    )

    try:
        response = requests.get(weather_url, timeout=10)
        data = response.json()

    except requests.exceptions.RequestException as e:
        print("Network/API Error:", e)
        return None

    hourly = data["hourly"]
    daily  = data["daily"]

    # Hour index: 9 = 9am, 15 = 3pm
    weather = {
        "MinTemp":      daily["temperature_2m_min"][0],
        "MaxTemp":      daily["temperature_2m_max"][0],
        "Humidity9am":  hourly["relativehumidity_2m"][9],
        "Humidity3pm":  hourly["relativehumidity_2m"][15],
        "Pressure9am":  hourly["surface_pressure"][9],
        "Pressure3pm":  hourly["surface_pressure"][15],
        "Temp9am":      hourly["temperature_2m"][9],
        "Temp3pm":      hourly["temperature_2m"][15],
        "WindSpeed9am": hourly["windspeed_10m"][9],
        "WindSpeed3pm": hourly["windspeed_10m"][15],
        "RainToday":    1 if daily["precipitation_sum"][0] > 0 else 0
    }

    return weather