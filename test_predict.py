

import requests
import json
from datetime import date

API_URL = "http://127.0.0.1:8000/predict"  # Change to deployed URL if needed

# Your custom patient data (fixed booleans, consistent keys)
# Your custom patient data (fixed booleans, consistent keys)
patients = {
    "patient-001": {
        "age": 40, "gender": "male", "height_cm": 180.0, "weight_kg": 85.0,
        "region": "Dar-es-salaam", "area": "Mbagala", "condition": "None",
        "income_lpa": 50.0, "smoker": False, "occupation": "private_job"
    },

    "patient-002": {
        "age": 35, "gender": "female", "height_cm": 165.0, "weight_kg": 70.0,
        "region": "Dar-es-salaam", "area": "Tandika",
        "condition": "Type 2 diabetes mellitus",
        "income_lpa": 50.0, "smoker": False, "occupation": "private_job"
    },

    "patient-003": {
        "age": 53, "gender": "female", "height_cm": 160.0, "weight_kg": 65.0,
        "region": "Dar-es-salaam", "area": "Msasani",
        "condition": "Asthma",
        "income_lpa": 50.0, "smoker": False, "occupation": "private_job"
    },

    "patient-004": {
        "age": 60, "gender": "male", "height_cm": 175.0, "weight_kg": 80.0,
        "region": "Dar-es-salaam", "area": "Kigamboni",
        "condition": "Low back pain",
        "income_lpa": 50.0, "smoker": False, "occupation": "retired"
    },

    "patient-005": {
        "age": 25, "gender": "female", "height_cm": 170.0, "weight_kg": 60.0,
        "region": "Dar-es-salaam", "area": "Kawe",
        "condition": "Generalized anxiety disorder",
        "income_lpa": 50.0, "smoker": False, "occupation": "private_job"
    },

    "patient-006": {
        "age": 25, "gender": "male", "height_cm": 56.0, "weight_kg": 71.0,
        "region": "Dar-es-salaam", "area": "Magomeni",
        "condition": "None",
        "income_lpa": 2.5, "smoker": False, "occupation": "private_job"
    },

    "patient-007": {
        "age": 34, "gender": "male", "height_cm": 178.0, "weight_kg": 71.0,
        "region": "Dar-es-salaam", "area": "Vingunguti",
        "condition": "Hypertension",
        "income_lpa": 62.4, "smoker": True, "occupation": "retired"
    }
}


for patient_id, p in patients.items():
    # Handle singular/plural region/area
    region = p.get("region") or p.get("regions", "")
    area = p.get("area") or p.get("areas", "")
    
    input_data = {
        "age": p["age"],
        "weight_kg": p["weight_kg"],
        "height_cm": p["height_cm"] / 100,  # Convert cm → meters (matches frontend/API)
        "income_lpa": p["income_lpa"],
        "smoker": p["smoker"],
        "region": region.strip().title(),
        "area": area.strip().title(),
        "occupation": p["occupation"]
    }
    
    try:
        response = requests.post(API_URL, json=input_data, timeout=5)
        response.raise_for_status()
        result = response.json()
        print(f"Prediction for {patient_id}: {result['premium_category']}")
        print(f"  Details: {result['input_received']}\n")
    except requests.exceptions.RequestException as e:
        print(f"Error for {patient_id}: {e}")















  
        







