


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

API_BASE = "http://127.0.0.1:8000"

# ---------------------------
# INIT PAGE STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "token" not in st.session_state:
    st.session_state.token = None

# ---------------------------
# HELPERS
# ---------------------------
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# ---------------------------
# LOGIN PAGE
# ---------------------------
def login_page():
    st.title("Insurance Premium Predictor")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            res = requests.post(
                f"{API_BASE}/token",
                data={"username": email, "password": password},
            )
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.session_state.page = "predict"
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()

# ---------------------------
# SIGNUP PAGE
# ---------------------------
def signup_page():
    st.title("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        res = requests.post(
            f"{API_BASE}/auth/register",
            json={"email": email, "password": password},
        )

        if res.status_code == 201:
            st.success("Account created successfully!")
            st.info("Now login using your email and password.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(res.text)

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------------------
# PREDICTION PAGE
# ---------------------------
def predictor_page():
    st.success("Logged in successfully")

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()

    st.subheader("Enter Your Details")

    age = st.number_input("Age", 1, 119, 30)
    height = st.number_input("Height (m)", 0.5, 2.5, 1.7)
    weight = st.number_input("Weight (kg)", 1.0, 200.0, 65.0)
    income_lpa = st.number_input("Annual Income (LPA)", 0.1, 100.0, 10.0)

    smoker = st.selectbox("Are you a smoker?", [True, False])

    condition = st.selectbox(
        "Existing Condition",
        ["none", "diabetes", "heart_disease", "asthma"]
    )

    region = st.text_input("Region", "Dar es Salaam")
    area = st.text_input("Area", "Mbagala")

    occupation = st.selectbox(
        "Occupation",
        [
            "private_job",
            "government_job",
            "business_owner",
            "freelancer",
            "student",
            "retired",
            "unemployed",
        ],
    )

    if st.button("Predict Premium"):
        payload = {
            "age": age,
            "gender": "male",  # can make this a selectbox later
            "height_cm": int(height * 100),
            "weight_kg": weight,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "condition": condition,
            "region": region,
            "area": area,
            "occupation": occupation,
        }

        res = requests.post(
            f"{API_BASE}/predict",
            json=payload,
            headers=auth_headers(),
        )

        if res.status_code == 200:
            st.success(
                f"Predicted Premium Category: **{res.json()['premium_category']}**"
            )
        else:
            st.error(res.text)


# ---------------------------
# MAIN
# ---------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "predict":
    predictor_page()






