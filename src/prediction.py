# ==============================
# PREDICTION SCRIPT
# ==============================
import os
import pickle
import numpy as np

# ==============================
# Dynamic Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "trained_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

# ==============================
# LOAD MODEL & SCALER
# ==============================

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(scaler_path, "rb") as f:
    scaler = pickle.load(f)


# ==============================
# PREDICTION FUNCTION
# ==============================

def predict_rain(input_data):
    """
    input_data: list of 11 features
    """

    import pandas as pd

    columns = ['MinTemp','MaxTemp','Humidity9am','Humidity3pm',
                'Pressure9am','Pressure3pm','Temp9am','Temp3pm',
                'WindSpeed9am','WindSpeed3pm','RainToday']

    input_df = pd.DataFrame([input_data], columns=columns)

    input_scaled = scaler.transform(input_df)

    # Predict
    prediction = model.predict(input_scaled)

    return prediction[0]