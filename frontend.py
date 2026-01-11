import streamlit as st
import requests

API_URL = "http://34.226.152.222/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
region = st.text_input("Region", value="Dar-es-salaam")
area = st.text_input("Area", value="Mbagala")
occupation = st.selectbox(
    "Occupation",
    [
        'retired', 'freelancer', 'student',
        'government_job', 'business_owner',
        'unemployed', 'private_job'
    ]
)

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income": income_lpa,   # ✅ fixed
        "smoker": smoker,
        "region": region,
        "area": area,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            st.success(
                f"Predicted Insurance Premium Category: **{result['premium_category']}**"
            )
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")




















