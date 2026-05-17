# Rain Prediction using Machine Learning 🌧️

A Machine Learning project that predicts whether it will rain tomorrow using historical weather data and real-time weather API integration.

---

# 📌 Project Overview

This project uses multiple Machine Learning algorithms to analyze weather conditions and predict rainfall. The system supports:

* Manual weather input prediction
* Live weather prediction using Open-Meteo API
* Data visualization and analysis
* PCA and clustering techniques

The project was developed as part of the **Applied Machine Learning** course.

---

# 🚀 Features

##  Machine Learning Models

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Decision Tree
* Random Forest
* Naive Bayes

---

##  Data Processing

* Missing value handling
* Feature selection
* Data scaling
* Encoding categorical data

---

##  Exploratory Data Analysis (EDA)

* Correlation Heatmaps
* Boxplots
* Distribution analysis
* Pairplots

---

##  Advanced ML Concepts

* PCA (Principal Component Analysis)
* K-Means Clustering
* Handling imbalanced data

---

##  Real-Time Weather Prediction

* Fetches live weather data using Open-Meteo API
* City-based weather prediction
* Manual + automatic prediction modes

---

# 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Requests API

---

# 📂 Project Structure

```text
Rain-Prediction-ML/
│
├── data/
│   └── weatherAUS.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── models/
│   ├── trained_model.pkl
│   └── scaler.pkl
│
├── src/
│   ├── training.py
│   ├── prediction.py
│   └── weather_api.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset

Dataset used:

* Rain in Australia Dataset

Dataset contains weather information such as:

* Temperature
* Humidity
* Pressure
* Wind Speed
* Rainfall

Target Variable:

* `RainTomorrow`

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <your-github-repo-link>
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Training Script

```bash
python src/training.py
```

---

## 4️⃣ Run Main Application

```bash
python main.py
```

---

# 🌐 API Integration

This project uses:

* Open-Meteo Forecast API
* Open-Meteo Geocoding API

Official Documentation:

* [Open-Meteo Forecast API Docs](https://open-meteo.com/en/docs?utm_source=chatgpt.com)
* [Open-Meteo Geocoding API Docs](https://open-meteo.com/en/docs/geocoding-api?utm_source=chatgpt.com)

---

# 🧠 Machine Learning Workflow

```text
Data Collection
       ↓
Data Cleaning
       ↓
EDA & Visualization
       ↓
Feature Selection
       ↓
Model Training
       ↓
Model Evaluation
       ↓
PCA & Clustering
       ↓
Real-Time Prediction System
```

---

# 📈 Best Performing Model

Random Forest performed best overall because:

* Handles nonlinear relationships effectively
* Reduces overfitting
* Works well with weather datasets

---

# 🎯 Future Improvements

* GUI using Tkinter or Streamlit
* Web deployment
* Better feature engineering
* Hyperparameter tuning
* Forecast prediction for multiple days

---

# 📷 Example Output

```text
1. Manual Weather Input
2. Automatic Weather Fetch (API)
3. Exit
```

```text
Prediction: It will RAIN tomorrow 🌧️
```

---

# 👨‍💻 Author

Developed as part of the Applied Machine Learning course project.
