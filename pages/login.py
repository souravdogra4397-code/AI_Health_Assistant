import streamlit as st
import re
from database import login_user

st.set_page_config(
    page_title="Login | AI Health Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- ADVANCED MEDICAL UI & ANIMATIONS ----------
st.markdown("""
<style>
/* Hide sidebar & header */
[data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] {
    display: none !important;
}

/* Background matched with dashboard + Smooth Load Animation */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    animation: fadeIn 1s ease-out;
}

/* Keyframe Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseGlow {
    0% { filter: drop-shadow(0 0 10px rgba(56,189,248,0.3)); transform: scale(1); }
    50% { filter: drop-shadow(0 0 25px rgba(56,189,248,0.7)); transform: scale(1.05); }
    100% { filter: drop-shadow(0 0 10px rgba(56,189,248,0.3)); transform: scale(1); }
}

/* Emoji Logo & Title Styling */
.logo-title-container {
    text-align: center;
    margin-top: 5vh;
    margin-bottom: 35px;
}

.emoji-logo {
    font-size: 4.5rem;
    margin-bottom: -5px;
    animation: pulseGlow 3s infinite alternate; /* Glowing animation */
    display: inline-block;
}

.title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    padding: 0;
    letter-spacing: 1px;
}

.subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-top: 5px;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Input Fields Styling (Premium Dark Mode Look) */
div[data-baseweb="input"] {
    background-color: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease-in-out !important;
}

div[data-baseweb="input"]:focus-within {
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.2) !important;
    background-color: rgba(15, 23, 42, 0.9) !important;
}

/* Primary Button Styling (Login) */
button[kind="primary"] {
    background: linear-gradient(90deg, #38bdf8, #34d399) !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    border: none !important;
    transition: all 0.3s ease !important;
    margin-top: 15px;
    padding: 10px !important;
}

button[kind="primary"]:hover {
    box-shadow: 0 5px 20px rgba(56, 189, 248, 0.4) !important;
    transform: translateY(-3px) scale(1.01) !important;
}

button[kind="primary"]:active {
    transform: translateY(0px) scale(0.98) !important;
}

/* Secondary Buttons Styling (Back & Register) */
button[kind="secondary"] {
    background-color: transparent !important;
    border: 1px solid #475569 !important;
    color: #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

button[kind="secondary"]:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    background-color: rgba(56, 189, 248, 0.05) !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGO & TITLE SECTION ----------
st.markdown("""
<div class="logo-title-container">
    <div class="emoji-logo">🏥</div>
    <h1 class="title">AI Health Assistant</h1>
    <div class="subtitle">Secure Medical Login Portal</div>
</div>
""", unsafe_allow_html=True)

# ---------- LOGIN FORM ----------
username = st.text_input("👤 Username (Letters & Numbers only)")
password = st.text_input("🔒 Password", type="password")

st.write("")

# Login button
if st.button("🔐 Login", type="primary", use_container_width=True):
    if not username or not password:
        st.warning("Please fill all fields.")
    elif not re.match("^[a-zA-Z0-9]+$", username):
        st.error("Username can only contain letters and numbers.")
    elif len(password) < 8:
        st.error("Password must be at least 8 characters long.")
    else:
        user = login_user(username, password)
        if user:
            st.success("Login Successful! Redirecting...")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Invalid Username or Password.")

st.write("")
st.divider()

# ---------- BOTTOM NAV BUTTONS ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/register.py")
        
