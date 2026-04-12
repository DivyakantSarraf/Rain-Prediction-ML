from src.prediction import predict_rain

print("=== Rain Prediction System ===")

MinTemp = float(input("Min Temperature: "))
MaxTemp = float(input("Max Temperature: "))
Humidity9am = float(input("Humidity at 9am: "))
Humidity3pm = float(input("Humidity at 3pm: "))
Pressure9am = float(input("Pressure at 9am: "))
Pressure3pm = float(input("Pressure at 3pm: "))
Temp9am = float(input("Temp at 9am: "))
Temp3pm = float(input("Temp at 3pm: "))
WindSpeed9am = float(input("Wind Speed at 9am: "))
WindSpeed3pm = float(input("Wind Speed at 3pm: "))
RainToday = int(input("Rain Today (1 = Yes, 0 = No): "))

input_data = [MinTemp, MaxTemp, Humidity9am, Humidity3pm,
              Pressure9am, Pressure3pm, Temp9am, Temp3pm,
              WindSpeed9am, WindSpeed3pm, RainToday]

result = predict_rain(input_data)

if result == 1:
    print("It will RAIN tomorrow")
else:
    print("No rain tomorrow")