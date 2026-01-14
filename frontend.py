


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

API_BASE = "http://172.232.112.57:8000"  # Consistent base URL (your live server)
API_URL = f"{API_BASE}/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

def get_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def login_page():
    st.title("🚀 Welcome to Register")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    if email and password:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                login_data = {"username": email, "password": password}
                response = requests.post(f"{API_BASE}/auth/jwt/login", data=login_data)
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    user_response = requests.get(f"{API_BASE}/users/me", headers=get_headers())
                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                    else:
                        st.error("Failed to get user info")
                else:
                    st.error("Invalid email or password!")
        with col2:
            if st.button("Sign Up", type="secondary", use_container_width=True):
                signup_data = {"email": email, "password": password}
                response = requests.post(f"{API_BASE}/auth/register", json=signup_data)
                if response.status_code == 201:
                    st.success("Account created! Click Login now.")
                else:
                    error_detail = response.json().get("detail", "Registration failed")
                    st.error(f"Registration failed: {error_detail}")
    else:
        st.info("Enter your email and password above")

# Show login if not authenticated
if "token" not in st.session_state:
    login_page()
else:
    # Logged in - show predictor form
    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    gender = st.selectbox("Gender", options=["male", "female"])
    weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01)
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
    smoker = st.selectbox("Are you a smoker?", options=[True, False], format_func=lambda x: "Yes" if x else "No")
    condition = st.selectbox("Pre-existing Medical Condition", options=["none", "diabetes", "hypertension", "heart_disease"])
    region = st.text_input("Region", value="Dar es Salaam").strip().title()  # Fixed capitalization
    area = st.text_input("Area", value="Mbagala").strip().title()
    occupation = st.selectbox(
        "Occupation",
        options=["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"]
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
                response = requests.post(API_URL, json=input_data, headers=get_headers(), timeout=10)
                response.raise_for_status()
                result = response.json()
                premium_keys = ["premium_category", "prediction", "premium", "category", "predicted_category"]
                premium = next((result.get(key) for key in premium_keys if key in result), None)
                if premium:
                    st.success(f"**Predicted Premium Category: {premium}**")
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
                    st.json(input_data)
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI server. Make sure it's running.")
            except requests.exceptions.HTTPError as e:
                st.error(f"API Error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")




                