from fastapi.testclient import TestClient
from app.app import app


client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "Insurance Premium Predictor API"

def test_predict_requires_auth():
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
    assert res.status_code == 401



####clones

