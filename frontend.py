


#import streamlit as st
#import requests

#API_URL = "http://127.0.0.1:8000/predict"


#st.title("Insurance Premium Category Predictor")
#st.markdown("Enter your details below:")

#age = st.number_input("Age", min_value=1, max_value=119, value=30)
#weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
#height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
#income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
#smoker = st.selectbox("Are you a smoker?", options=[True, False])
#region = st.text_input("Region", value="Dar-es-salaam")
#area = st.text_input("Area", value="Mbagala")
#occupation = st.selectbox(
#    "Occupation",
#    [
#        'retired', 'freelancer', 'student',
#        'government_job', 'business_owner',
#        'unemployed', 'private_job'
#    ]
#)

#if st.button("Predict Premium Category"):
#    input_data = {
#        "age": age,
#        "weight": weight,
#        "height": height,
#        "income": income_lpa,   # ✅ fixed
#        "smoker": smoker,
#       "region": region,
#        "area": area,
#        "occupation": occupation
#    }

#    try:
#        response = requests.post(API_URL, json=input_data)
#      if response.status_code == 200:
#           result = response.json()
#            st.success(
#                f"Predicted Insurance Premium Category: **{result['premium_category']}**"
#            )
#        else:
#            st.error(f"API Error: {response.status_code}")
#           st.write(response.text)

#   except requests.exceptions.ConnectionError:
#       st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")









import streamlit as st
import requests

API_URL = "http://172.232.112.57:8000/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
gender = st.selectbox(
    "Gender",
    options=["male", "female"]
)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input(
    "Height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01
)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False],
    format_func=lambda x: "Yes" if x else "No"
)
condition = st.selectbox(
    "Pre-existing Medical Condition",
    options=["none", "diabetes", "hypertension", "heart_disease"]
)
region = st.text_input("Region", value="Dar-es-salaam").strip().title()
area = st.text_input("Area", value="Mbagala").strip().title()
occupation = st.selectbox(
    "Occupation",
    options=[
        "retired", "freelancer", "student",
        "government_job", "business_owner",
        "unemployed", "private_job"
    ]
)

if st.button("Predict Premium Category"):
    if not region or not area:
        st.warning("Please enter a valid region and area.")
    else:
        input_data = {
            "age": age,
            "gender": gender,
            "height_cm": int(height * 100),
            "weight_kg": weight,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "condition": condition,
            "region": region,
            "area": area,
            "occupation": occupation
        }
        try:
            response = requests.post(API_URL, json=input_data, timeout=10)
            response.raise_for_status()
            result = response.json()
            # Enhanced premium extraction with new key
            premium_keys = ["premium_category", "prediction", "premium", "category", "predicted_category"]
            premium = next((result.get(key) for key in premium_keys if key in result), None)
            if premium:
                st.success(f"**Predicted Premium Category: {premium}**")
                # Optional: Display confidence/probs if available
                confidence = result.get("confidence")
                probs = result.get("class_probabilities")
                if confidence:
                    st.info(f"Confidence: {confidence:.2f}")
                if probs:
                    st.write("Class Probabilities:")
                    st.json(probs)
            else:
                st.error("❌ API response did not include a premium category")
            with st.expander("Full API Response (for debugging)"):
                st.json(result)
            with st.expander("Input Details"):
                st.json(input_data)  # Show input for verification
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to FastAPI server. Make sure it's running on port 8000.")
        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")











            