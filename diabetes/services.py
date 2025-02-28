import joblib
import numpy as np
import pandas as pd
import os
import sklearn

# Print sklearn version for debugging
print("SKLearn:", sklearn.__version__)

# Define relative path to the model
modelo_path = os.path.join(os.path.dirname(__file__), "..", "Analisis&Modelos", "modelo_rl.pkl")

# Load model with error handling
try:
    modelo = joblib.load(modelo_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    modelo = None

FEATURE_NAME_MAPPING = {
    "glucose": "Glucose",
    "blood_pressure": "BloodPressure",
    "skin_thickness": "SkinThickness",
    "insulin": "Insulin",
    "bmi": "BMI",
    "diabetes_pedigree_function": "DiabetesPedigreeFunction",
    "age": "Age"
}

def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age):
    if modelo is None:
        print("Model not loaded. Cannot make predictions.")
        return None

    try:
        # Create a DataFrame with correct feature names
        input_data = pd.DataFrame([[
            glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age
        ]], columns=FEATURE_NAME_MAPPING.keys())

        # Rename columns to match the trained model's feature names
        input_data = input_data.rename(columns=FEATURE_NAME_MAPPING)

        # Make prediction (probability of diabetes)
        prediction = modelo.predict_proba(input_data)[:, 1]

        print("Prediction:", prediction[0])
        return float(prediction[0])  # Convert to standard float
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None
