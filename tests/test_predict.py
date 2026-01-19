from fastapi.testclient import TestClient
from app.app import app  # Assuming this is correct based on your structure

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "Insurance Premium Prediction API"

def test_predict_requires_auth():
    # Test without token – expect 401 Unauthorized
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
    assert res.status_code == 401  # Expect failure without auth
    assert "detail" in res.json()
    assert res.json()["detail"] == "Not authenticated"  # Or your custom message








