from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, MODEL_VERSION

import os
import pickle
import pandas as pd


# =========================
# App initialization
# =========================
app = FastAPI(title="Insurance Premium Prediction API")


# =========================
# Load ML model (ONCE)
# =========================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError(
        f"Model file not found at {MODEL_PATH}. Train the model first."
    )


# =========================
# Utility functions
# =========================
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def age_to_group(age: int) -> str:
    if age < 18:
        return "child"
    elif age < 35:
        return "young_adult"
    elif age < 60:
        return "adult"
    return "senior"


# =========================
# Routes
# =========================

# Human-readable
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}


# Machine-readable
@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "version": MODEL_VERSION,
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):

    # =========================
    # Feature engineering
    # =========================


    user_input = {
        # engineered features
        "bmi": calculate_bmi(data.weight_kg, data.height_cm),
        "age_group": age_to_group(data.age),
        "lifestyle_risk": "medium",      # placeholder (logic later)
        "city_tier": "tier_1",            # placeholder
        "income_lpa": 8.5,                # placeholder
        "occupation": "office_worker",    # placeholder
        # raw features


        "age": data.age,
        "gender": data.gender,
        "height_cm": data.height_cm,
        "weight_kg": data.weight_kg,
        "city": data.city,
        "state": data.state,
        "condition": data.condition,
    }

    try:
        # 🔥 THIS WAS MISSING
        predicted_category, confidence, class_probabilities = predict_output(
            model, user_input
        )

        return {
            "predicted_category": predicted_category,
            "confidence": float(confidence),
            "class_probabilities": {
                k: float(v) for k, v in class_probabilities.items()
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




#Hypertension                    1
#Type 2 diabetes mellitus        1
#Asthma                          1
#Low back pain                   1
#Generalized anxiety disorder








