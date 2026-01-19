from fastapi.testclient import TestClient
from app.app import app  # Assuming this is correct based on your structure

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "Insurance Premium Prediction API"

def test_predict_no_auth_needed():
    res = client.post("/predict", json={
        "age": 30,
        "gender": "male",
        "height_cm": 180,
        "weight_kg": 70,
        "income_lpa": 10,
        "smoker": False,
        "condition": "None",
        "region": "Dar es Salaam",
        "area": "Mbagala",
        "occupation": "private_job"
    })
    assert res.status_code == 200  # No auth in app, so expect success
    data = res.json()
    assert "predicted_category" in data  # Matches your app's response key
    assert "confidence" in data
    assert "class_probabilities" in data









