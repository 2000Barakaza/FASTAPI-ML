import pickle
import pandas as pd
import os

# import the ml model
# Directory of predict.py → FASTAPI+ML/model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root → FASTAPI+ML
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Path to model.pkl (in project root)
MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found at {MODEL_PATH}. "
        "Make sure model.pkl exists in the project root."
    )

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# MLFlow
MODEL_VERSION = '1.0.0'

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }











