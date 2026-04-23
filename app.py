# app.py
# Author: Sourav
import streamlit as st
from database import create_tables

# Run DB setup on start
create_tables()

st.set_page_config(page_title="AI Health Assistant", page_icon="⚕️", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
#     NEW PREMIUM CSS & ANIMATIONS
# ==========================================
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0f2027, #203a43);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e2e8f0;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .fade-in {
        animation: fadeIn 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        opacity: 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-title {
        font-size: 4.8rem;
        font-weight: 900;
        text-align: center;
        margin-top: 8vh;
        background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 50px;
    }

    button[kind="primary"] {
        background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%) !important;
        color: #0f172a !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
    }

    button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
#         TOP NAVIGATION BAR
# ==========================================
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])

with c1:
    st.markdown("<h3 style='color: white;'>🩺 Health AI</h3>", unsafe_allow_html=True)

with c2:
    if st.button("About Us", use_container_width=True):
        st.switch_page("pages/about.py")

with c3:
    if st.button("Contact", use_container_width=True):
        st.switch_page("pages/contact.py")

with c4:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/login.py")

with c5:
    if st.button("Register", use_container_width=True):
        st.switch_page("pages/register.py")

# ==========================================
#         MAIN HERO SECTION (FIXED TEXT)
# ==========================================
st.markdown("<div class='main-title fade-in'>Next-Gen Healthcare,<br>Powered by AI.</div>", unsafe_allow_html=True)

st.markdown("<div class='sub-title fade-in'>Instant symptom analysis. Smart disease prediction. Secure medical history.<br>Experience the future of personal health.</div>", unsafe_allow_html=True)

# ==========================================
#      GET STARTED BUTTON
# ==========================================
col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    if st.button("🩺 Start Your Diagnosis", type="primary", use_container_width=True):
        st.switch_page("pages/login.py")

# ==========================================
#         FOOTER
# ==========================================
st.markdown("<hr>", unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns([2, 1.5, 1.5, 2, 0.1])

with f2:
    if st.button("Privacy Policy", use_container_width=True):
        st.switch_page("pages/privacy.py")

with f3:
    if st.button("Terms & Conditions", use_container_width=True):
        st.switch_page("pages/terms.py")

st.markdown("<p style='text-align: center;'>© 2026 AI Health Assistant</p>", unsafe_allow_html=True)