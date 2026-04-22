# pages/register.py
import streamlit as st
import re
import datetime
from database import add_user

st.set_page_config(
    page_title="Register | AI Health Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- ADVANCED MEDICAL UI (Matched with Dashboard/Login) ----------
st.markdown("""
<style>
/* Hide sidebar & header */
[data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] {
    display: none !important;
}

/* Background matched with dashboard */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Emoji Logo & Title Styling */
.logo-title-container {
    text-align: center;
    margin-top: 5vh;
    margin-bottom: 35px;
}
.emoji-logo {
    font-size: 4.5rem;
    margin-bottom: -10px;
    filter: drop-shadow(0px 0px 10px rgba(56,189,248,0.4));
}
.title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    padding: 0;
}
.subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-top: 5px;
}

/* Primary Button Styling */
button[kind="primary"] {
    background: linear-gradient(90deg, #38bdf8, #34d399) !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    border: none !important;
    transition: 0.3s;
    margin-top: 15px;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.5) !important;
    transform: translateY(-2px);
}

/* Secondary Button Styling */
button[kind="secondary"] {
    border-radius: 12px;
    border: 1px solid #38bdf8;
    color: #38bdf8;
    background: transparent;
    transition: 0.3s;
}
button[kind="secondary"]:hover {
    background: rgba(56, 189, 248, 0.1);
    border-color: #34d399;
    color: #34d399;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGO & TITLE SECTION ----------
st.markdown("""
<div class="logo-title-container">
    <div class="emoji-logo">🏥</div>
    <h1 class="title">Create Account</h1>
    <div class="subtitle">Join AI Health Assistant</div>
</div>
""", unsafe_allow_html=True)

# ---------- FORM ----------
colA, colB = st.columns(2)

with colA:
    email = st.text_input("📧 Email Address")
    phone = st.text_input("📱 Phone Number (10 digits)")

with colB:
    min_date = datetime.date(1926, 1, 1)
    max_date = datetime.date.today()
    dob = st.date_input(
        "📅 Date of Birth",
        value=datetime.date(2000, 1, 1),
        min_value=min_date,
        max_value=max_date
    )

st.write("")

colC, colD = st.columns(2)

with colC:
    username = st.text_input("👤 Username")

with colD:
    password = st.text_input("🔒 Password (Min 8 Characters)", type="password")

st.write("")

# ---------- REGISTER BUTTON ----------
if st.button("📝 Register Now", type="primary", use_container_width=True):
    if not email or not phone or not username or not password:
        st.warning("Please fill in all the fields.")
    elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        st.error("Please enter a proper email address.")
    elif not phone.isdigit() or len(phone) != 10:
        st.error("Phone number must be exactly 10 digits.")
    elif len(password) < 8:
        st.error("Password must be at least 8 characters long.")
    else:
        if add_user(email, phone, str(dob), username, password):
            st.success("Account created successfully! Redirecting...")
            st.balloons()
        else:
            st.error("Username already exists.")

st.write("")
st.divider()

# ---------- BACK BUTTON ----------
if st.button("⬅️ Back to Login", use_container_width=True):
    st.switch_page("pages/login.py")