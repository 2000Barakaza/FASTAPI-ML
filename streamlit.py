import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="wide",
)

API_BASE = "http://127.0.0.1:8000"

# ---------------------------
# INIT PAGE STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "subscription_status" not in st.session_state:
    st.session_state.subscription_status = None
if "subscription_plan" not in st.session_state:
    st.session_state.subscription_plan = "free"

# ---------------------------
# HELPERS
# ---------------------------
def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def fetch_user_info():
    res = requests.get(f"{API_BASE}/users/me", headers=auth_headers())
    if res.status_code == 200:
        data = res.json()
        st.session_state.role = data.get("role", "user")
        # Hardcode admin role for specific email (for development/testing purposes only)
        if data.get("email") == "manjale2021@gmail.com":
            st.session_state.role = "admin"
        sub = data.get("subscription", {})
        st.session_state.subscription_plan = sub.get("plan", "free")
        st.session_state.subscription_status = sub.get("status", "free")
        return data
    return None

def fetch_predictions():
    res = requests.get(f"{API_BASE}/predictions/me", headers=auth_headers())
    if res.status_code == 200:
        return res.json()
    return []

# ---------------------------
# LOGIN PAGE
# ---------------------------
def login_page():
    st.title("🔐 Login")
    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            identifier = st.text_input("Email or Username")
        with col2:
            password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
    if submit:
        res = requests.post(f"{API_BASE}/token", data={"username": identifier, "password": password})
        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials or account not verified")

# ---------------------------
# SIGNUP PAGE
# ---------------------------
def signup_page():
    st.title("📝 Create Account")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Create Account")
    if submit:
        res = requests.post(f"{API_BASE}/auth/register", json={"email": email, "password": password})
        if res.status_code == 201:
            st.success("Account created! Check your email to verify.")
        else:
            st.error(res.json().get("detail", "Registration failed"))

# ---------------------------
# VERIFY EMAIL PAGE
# ---------------------------
def verify_email_page():
    st.title("✅ Verify Your Email")
    token = st.text_input("Enter verification token from email")
    if st.button("Verify"):
        res = requests.get(f"{API_BASE}/auth/verify-email?token={token}")
        if res.status_code == 200:
            st.success("Email verified! You can now log in.")
        else:
            st.error("Invalid or expired token")

# ---------------------------
# PREDICTOR PAGE (FOR USERS AND ADMINS)
# ---------------------------
def predictor_page():
    st.title("📊 Predict Insurance Premium")
    if (
        st.session_state.role != "admin"
        and st.session_state.subscription_plan != "premium"
    ):
        st.warning("🔒 You need an active premium subscription to predict.")
        st.stop()
    with st.form("predict_form"):
        st.subheader("👤 Personal Info")
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", 1, 119, 30)
        with c2:
            height = st.number_input("Height (m)", 0.5, 2.5, 1.7)
        with c3:
            weight = st.number_input("Weight (kg)", 1.0, 200.0, 65.0)
        st.subheader("💼 Lifestyle & Income")
        c4, c5, c6 = st.columns(3)
        with c4:
            income_lpa = st.number_input("Income (LPA)", 0.1, 100.0, 10.0)
        with c5:
            smoker = st.selectbox("Smoker?", [True, False])
        with c6:
            occupation = st.selectbox(
                "Occupation",
                ["private_job", "government_job", "business_owner", "freelancer", "student", "retired", "unemployed"]
            )
        st.subheader("📍 Health & Location")
        c7, c8, c9 = st.columns(3)
        with c7:
            condition = st.selectbox("Condition", ["none", "diabetes", "heart_disease", "asthma"])
        with c8:
            region = st.text_input("Region", "Dar es Salaam")
        with c9:
            area = st.text_input("Area", "Mbagala")
        submit = st.form_submit_button("🚀 Predict Premium", use_container_width=True)
    if submit:
        payload = {
            "age": age,
            "gender": "male",
            "height_cm": int(height * 100),
            "weight_kg": weight,
            "income_lpa": income_lpa,
            "smoker": smoker,
            "condition": condition,
            "region": region,
            "area": area,
            "occupation": occupation,
        }
        with st.spinner("Predicting..."):
            res = requests.post(f"{API_BASE}/predict", json=payload, headers=auth_headers())
        if res.status_code == 200:
            result = res.json()
            st.success(f"Predicted Premium Category: **{result['premium_category']}**")
            st.info(f"Your BMI: **{result['bmi']:.2f}**")
            st.balloons()
        else:
            st.error(res.json().get("detail", "Prediction failed"))

# ---------------------------
# SUBSCRIPTION PAGE
# ---------------------------
def subscription_page():
    st.title("💳 Subscription Management")
    user = fetch_user_info()
    sub = user.get("subscription") if user else None
    if sub:
        st.success(f"Current Plan: **{sub['plan'].title()}**")
        st.info(f"Status: {sub['status'].title()} | Expires: {sub.get('end_date', 'Never')}")
    else:
        st.info("You have no active subscription.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Available Plans")
        st.write("**Free** - Limited predictions")
        st.write("**Premium** - Unlimited predictions + priority support")
    with col2:
        plan = st.selectbox("Choose Plan", ["free", "premium"])
        if st.button("Upgrade / Change Plan", use_container_width=True):
            with st.spinner("Processing..."):
                res = requests.post(
                    f"{API_BASE}/subscriptions/upgrade",
                    json={"plan": plan},
                    headers=auth_headers()
                )
            if res.status_code == 200:
                st.success("Plan updated successfully!")
                fetch_user_info()  # Refresh status
                st.rerun()
            else:
                st.error("Failed to update plan")

# ---------------------------
# PREDICTION HISTORY PAGE
# ---------------------------
def history_page():
    st.title("📜 Your Prediction History")
    predictions = fetch_predictions()
    if predictions:
        df = pd.DataFrame(predictions)
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
        df = df[["created_at", "premium_category", "bmi"]]  # Assuming 'risk' was 'premium_category'
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No predictions yet. Make your first prediction!")

# ---------------------------
# ADMIN DASHBOARD PAGE
# ---------------------------
def admin_page():
    st.title("👑 Admin Dashboard")
    res = requests.get(f"{API_BASE}/admin/stats", headers=auth_headers())
    if res.status_code == 200:
        stats = res.json()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Users", stats["total_users"])
        c2.metric("Active Users", stats["active_users"])
        c3.metric("Total Subscriptions", stats["subscriptions"])
        c4.metric("Active Subscriptions", stats["active_subscriptions"])
        daily_res = requests.get(f"{API_BASE}/admin/predictions/daily", headers=auth_headers())
        if daily_res.status_code == 200:
            daily = daily_res.json()
            st.subheader("Daily Predictions")
            chart_data = pd.DataFrame(daily)
            st.line_chart(chart_data.set_index("date")["count"])
    else:
        st.error("Failed to load dashboard data")
    # Additional admin features, e.g., view users
    if st.button("View All Users"):
        res = requests.get(
            f"{API_BASE}/users",
            headers=auth_headers(),
        )
        if res.status_code == 200:
            users = res.json()
            st.write("Users:")
            for user in users:
                st.write(f"- {user['email']} (Role: {user.get('role', 'user')})")
        else:
            st.error("Failed to fetch users")

# ---------------------------
# MAIN
# ---------------------------
st.sidebar.title("🧭 Menu")

if st.session_state.token:
    fetch_user_info()
    pages = ["Predict", "Subscription", "Prediction History", "Logout"]
    if st.session_state.role == "admin":
        pages.insert(0, "Admin Dashboard")
    selected_page = st.sidebar.radio("Navigate", pages)
    # Debug info (remove in production)
    st.sidebar.write("**Debug**")
    st.sidebar.write(f"Role: {st.session_state.role}")
    st.sidebar.write(f"Plan: {st.session_state.subscription_plan}")
    st.sidebar.write(f"Status: {st.session_state.subscription_status}")
    if selected_page == "Logout":
        st.session_state.clear()
        st.rerun()
    elif selected_page == "Predict":
        predictor_page()
    elif selected_page == "Subscription":
        subscription_page()
    elif selected_page == "Prediction History":
        history_page()
    elif selected_page == "Admin Dashboard":
        admin_page()
else:
    pages = ["Login", "Sign Up", "Verify Email"]
    selected_page = st.sidebar.radio("Navigate", pages)
    if selected_page == "Login":
        login_page()
    elif selected_page == "Sign Up":
        signup_page()
    elif selected_page == "Verify Email":
        verify_email_page()









