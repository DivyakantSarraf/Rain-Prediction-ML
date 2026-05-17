from src.prediction import predict_rain
from src.weather_api import get_weather_data


# =========================================
# MANUAL INPUT FUNCTION
# =========================================

def manual_prediction():

    print("\n=== Manual Weather Input ===")

    MinTemp      = float(input("Min Temperature: "))
    MaxTemp      = float(input("Max Temperature: "))
    Humidity9am  = float(input("Humidity at 9am: "))
    Humidity3pm  = float(input("Humidity at 3pm: "))
    Pressure9am  = float(input("Pressure at 9am: "))
    Pressure3pm  = float(input("Pressure at 3pm: "))
    Temp9am      = float(input("Temp at 9am: "))
    Temp3pm      = float(input("Temp at 3pm: "))
    WindSpeed9am = float(input("Wind Speed at 9am: "))
    WindSpeed3pm = float(input("Wind Speed at 3pm: "))
    RainToday    = int(input("Rain Today (1 = Yes, 0 = No): "))

    input_data = [
        MinTemp, MaxTemp,
        Humidity9am, Humidity3pm,
        Pressure9am, Pressure3pm,
        Temp9am, Temp3pm,
        WindSpeed9am, WindSpeed3pm,
        RainToday
    ]

    result = predict_rain(input_data)
    print_result(result)


# =========================================
# API PREDICTION FUNCTION
# =========================================

def api_prediction():

    print("\n=== Live Weather Prediction ===")

    location     = input("Enter City Name (e.g. Panaji, Mumbai, Delhi): ")
    country_code = input("Enter Country Code (default IN): ").strip() or "IN"

    weather = get_weather_data(location, country_code)

    if weather is None:
        print("Could not fetch weather data.")
        return

    print("\nLive Weather Data:")
    for key, value in weather.items():
        print(f"  {key}: {value}")

    input_data = [
        weather["MinTemp"],
        weather["MaxTemp"],
        weather["Humidity9am"],
        weather["Humidity3pm"],
        weather["Pressure9am"],
        weather["Pressure3pm"],
        weather["Temp9am"],
        weather["Temp3pm"],
        weather["WindSpeed9am"],
        weather["WindSpeed3pm"],
        weather["RainToday"]
    ]

    result = predict_rain(input_data)
    print_result(result)


# =========================================
# PRINT RESULT
# =========================================

def print_result(result):

    print("\n===================================")

    if result == 1:
        print("Prediction: It will RAIN tomorrow")
    else:
        print("Prediction: No rain tomorrow")

    print("===================================")


# =========================================
# MAIN MENU
# =========================================

while True:

    print("\n===================================")
    print("      RAIN PREDICTION SYSTEM")
    print("===================================")
    print("1. Manual Weather Input")
    print("2. Automatic Weather Fetch (API)")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        manual_prediction()

    elif choice == "2":
        api_prediction()

    elif choice == "3":
        print("Exiting system")
        break

    else:
        print("Invalid choice! Please try again.")