from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.region_tier import regions, areas
from model.predict import predict_output, MODEL_VERSION, model
import os
import pickle
import pandas as pd

# =========================
# App initialization
# =========================
app = FastAPI(title="Insurance Premium Prediction API")

# =========================
# Pydantic Model
# =========================
class UserInput(BaseModel):
    # ======================
    # Raw input fields
    # ======================
    age: Annotated[int, Field(gt=0, lt=120, description="Age of the user")]
    gender: Annotated[str, Field(description="Gender of the user")]
    height_cm: Annotated[float, Field(gt=0, lt=250, description="Height in cm")]
    weight_kg: Annotated[float, Field(gt=0, description="Weight in kg")]
    region: Annotated[str, Field(description="Region")]
    area: Annotated[str, Field(description="Area")]
    condition: Annotated[str, Field(description="Medical condition")]
    income_lpa: Annotated[float, Field(gt=0, description="Income in LPA")]
    smoker: Annotated[bool, Field(description="Is smoker")]
    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        Field(description="Occupation"),
    ]
    # ======================
    # Validators
    # ======================
    @field_validator("region")
    def normalize_region(cls, v: str) -> str:
        return v.strip().title()
    @field_validator("area")
    def normalize_area(cls, v: str) -> str:
        return v.strip().title()
    # ======================
    # Computed fields
    # ======================
    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        return "low"
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    @computed_field
    @property
    def region_tier(self) -> int:
        if self.region in regions:
            return 1
        elif self.area in areas:
            return 2
        return 3

class PredictionResponse(BaseModel):
    predicted_category: str
    confidence: float
    class_probabilities: dict[str, float]

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
    user_input = {
        # engineered features
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        # map API fields to old model columns
        "region": data.region,        # was region
        "region_tier": data.region_tier, # was region_tier
        "area": data.area,         # was area
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
        # raw features
        "age": data.age,
        "gender": data.gender,
        "height_cm": data.height_cm,
        "weight_kg": data.weight_kg,
        "condition": data.condition,
    }
    try:
        return predict_output(user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









