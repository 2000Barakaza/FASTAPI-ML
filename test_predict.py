import requests
import json
from datetime import date

API_URL = "http://127.0.0.1:8000/predict"  # Change to your remote URL if deployed

# FHIR data (paste your JSON here)
fhir_data = [...]  # Paste the full list from your query

current = date(2026, 1, 1)

for p in fhir_data:
    name = p["name"][0]
    address = p["address"][0]
    telecom = p["telecom"][0]
    contact_str = telecom["value"] if telecom["system"] == "phone" else "0"
    contact = float(''.join(c for c in contact_str if c.isdigit() or c == '.')) or 0.0
    condition = p["conditions"][0]["display"]
    hypertension = "hypertension" in condition.lower()
    birth = date.fromisoformat(p["birthDate"])
    age = current.year - birth.year - ((current.month, current.day) < (birth.month, birth.day))
    
    input_data = {
        "age": age,
        "weight_kg": p["weight"],
        "height_cm": p["height"],  # cm, as fixed in app.py
        "contact": contact,
        "hypertension": hypertension,
        "city": address["city"],
        "state": address["state"],
        "gender": p["gender"] if p["gender"] in ["male", "female"] else "others",
        "condition": condition,
        "occupation": "private_job"  # Assume; change as needed
    }
    
    response = requests.post(API_URL, json=input_data)
    if response.status_code == 200:
        print(f"Prediction for {p['id']}: {response.json()}")
    else:
        print(f"Error for {p['id']}: {response.text}")













  
        