# ==============================
# PREDICTION SCRIPT
# ==============================

import pickle
import numpy as np


# ==============================
# LOAD MODEL & SCALER
# ==============================

with open("Rain-Prediction-ML/models/trained_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("Rain-Prediction-ML/models/scaler.pkl", "rb") as f:
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