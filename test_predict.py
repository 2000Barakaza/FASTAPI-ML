

#import requests
#import json
#from datetime import date

#API_URL = "http://127.0.0.1:8000/predict"  # Change to your remote URL if deployed

# FHIR data (paste your JSON here)
#fhir_data = [
#{
#  "patient-001": {
#    "age": 40,
#    "gender": "male",
#    "height_cm": 180.0,
#    "weight_kg": 85.0,
#    "region": "Dar-es-salaam",
#    "area": "Mbagala",
#    "condition": "None",
#    "income_lpa": 50.0,
#    "smoker": false,
#    "occupation": "private_job",
#    "bmi": 26.23,
#    "lifestyle_risk": "low",
#   "age_group": "adult",
#   "region_tier": 3
#  },
#  "patient-002": {
#    "age": 35,
#    "gender": "female",
#    "height_cm": 165.0,
#    "weight_kg": 70.0,
#    "region": "Dar-es-salaam",
#   "area": "Tandika",
#    "condition": "Type 2 diabetes mellitus",
#   "income_lpa": 50.0,
#    "smoker": false,
#   "occupation": "private_job",
#   "bmi": 25.71,
#    "lifestyle_risk": "low",
#    "age_group": "adult",
#    "region_tier": 3
# },
# "patient-003": {
#   "age": 53,
#    "gender": "female",
#    "height_cm": 160.0,
#    "weight_kg": 65.0,
#    "region": "Dar-es-salaam",
#    "area": "Msasani",
#    "condition": "Asthma",
#    "income_lpa": 50.0,
#    "smoker": false,
#    "occupation": "private_job",
#    "bmi": 25.39,
#    "lifestyle_risk": "low",
#    "age_group": "middle_aged",
#    "region_tier": 3
#  },
#  "patient-004": {
#    "age": 60,
#    "gender": "male",
#    "height_cm": 175.0,
#    "weight_kg": 80.0,
#    "region": "Dar-es-salaam",
#    "area": "Kigamboni",
#    "condition": "Low back pain",
#    "income_lpa": 50.0,
#    "smoker": false,
#   "occupation": "retired",
#   "bmi": 26.12,
#    "lifestyle_risk": "low",
#    "age_group": "senior",
#    "region_tier": 3
#  },
#  "patient-005": {
#    "age": 25,
#    "gender": "female",
#    "height_cm": 170.0,
#    "weight_kg": 60.0,
#    "region": "Dar-es-salaam",
#    "area": "Kawe",
#    "condition": "Generalized anxiety disorder",
#    "income_lpa": 50.0,
#    "smoker": false,
#    "occupation": "private_job",
#    "bmi": 20.76,
#    "lifestyle_risk": "low",
#    "age_group": "adult",
#    "region_tier": 3
#  },
#  "patient-006": {
    "age": 25,
    "gender": "male",
    "height_cm": 56.0,
    "weight_kg": 71.0,
    "region": "Dar-es-salaam",
    "area": "Magomeni",
    "condition": "None",
    "income_lpa": 2.5,
    "smoker": false,
    "occupation": "private_job",
    "bmi": 226.4,
    "lifestyle_risk": "medium",
    "age_group": "adult",
    "region_tier": 3
  },
#  "PATIENT-007": {
#    "age": 34,
#    "gender": "male",
#    "height_cm": 178.0,
#    "weight_kg": 71.0,
#   "regions": "Dar-Es-Salaam",
#    "areas": "Vingunguti",
#    "condition": "Hypertension",
#    "income_lpa": 62.4,
#    "smoker": true,
#    "occupation": "retired",
#    "bmi": 22.41,
#    "lifestyle_risk": "medium",
#    "age_group": "adult",
#    "region_tier": 2
#  }
#}
#]  # Paste the full list from your query
#
#current = date(2026, 1, 24)

#for p in fhir_data:
#    name = p["name"][0]
#    address = p["address"][0]
#    telecom = p["telecom"][0]
#    contact_str = telecom["value"] if telecom["system"] == "phone" else "0"
#    contact = float(''.join(c for c in contact_str if c.isdigit() or c == '.')) or 0.0
#   condition = p["conditions"][0]["display"]
#    hypertension = "hypertension" in condition.lower()
#    birth = date.fromisoformat(p["birthDate"])
#    age = current.year - birth.year - ((current.month, current.day) < (birth.month, birth.day))

#    input_data = {
 #       "age": age,
  #      "weight_kg": p["weight"],
  #      "height_cm": p["height"],  # cm, as fixed in app.py
  #      "contact": contact,
  #      "hypertension": hypertension,
  #      "region": address["region"],
  #      "area": address["area"],
  #      "gender": p["gender"] if p["gender"] in ["male", "female"] else "others",
  #      "condition": condition,
  #      "occupation": "private_job"  # Assume; change as needed
  #  }
    
  #  response = requests.post(API_URL, json=input_data)
  #  if response.status_code == 200:
  #      print(f"Prediction for {p['id']}: {response.json()}")
  #  else:
#        print(f"Error for {p['id']}: {response.text}")







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
        "weight": p["weight_kg"],
        "height": p["height_cm"] / 100,  # Convert cm → meters (matches frontend/API)
        "income": p["income_lpa"],
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



















  
        

