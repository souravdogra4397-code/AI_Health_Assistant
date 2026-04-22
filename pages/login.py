# pages/login.py
import streamlit as st
import re
from database import login_user

st.set_page_config(
    page_title="Login | AI Health Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- ADVANCED MEDICAL UI (Matched with Dashboard) ----------
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