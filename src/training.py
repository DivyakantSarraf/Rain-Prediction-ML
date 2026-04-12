# ==============================
# TRAINING SCRIPT
# ==============================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle


# ==============================
# LOAD DATA
# ==============================

data = pd.read_csv("Rain-Prediction-ML/data/weatherAUS.csv")


# ==============================
# DATA PREPROCESSING
# ==============================

# Drop unnecessary columns
data = data.drop(['Evaporation', 'Sunshine', 'Cloud9am', 'Cloud3pm'], axis=1)

# Drop rows with missing target
data = data.dropna(subset=['RainTomorrow'])

# Clean categorical values
data['RainTomorrow'] = data['RainTomorrow'].str.strip()
data['RainToday'] = data['RainToday'].str.strip()

# Convert to numeric
data['RainTomorrow'] = data['RainTomorrow'].map({'Yes': 1, 'No': 0})
data['RainToday'] = data['RainToday'].map({'Yes': 1, 'No': 0})

# Fill missing values
num_cols = data.select_dtypes(include=['float64', 'int64']).columns
data[num_cols] = data[num_cols].fillna(data[num_cols].mean())

cat_cols = data.select_dtypes(include=['object', 'string']).columns
data[cat_cols] = data[cat_cols].fillna(data[cat_cols].mode().iloc[0])


# ==============================
# FEATURE SELECTION
# ==============================

X = data[['MinTemp','MaxTemp','Humidity9am','Humidity3pm',
          'Pressure9am','Pressure3pm','Temp9am','Temp3pm',
          'WindSpeed9am','WindSpeed3pm','RainToday']]

y = data['RainTomorrow']


# ==============================
# TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ==============================
# SCALING
# ==============================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ==============================
# TRAIN MODEL (FINAL MODEL)
# ==============================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# ==============================
# SAVE MODEL
# ==============================

with open("Rain-Prediction-ML/models/trained_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("Rain-Prediction-ML/models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)


print("Model training complete and saved!")