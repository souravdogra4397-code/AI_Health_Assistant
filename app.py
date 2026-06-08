# app.py
# Author: Sourav
import streamlit as st
from database import create_tables

# Run DB setup on start
create_tables()

st.set_page_config(page_title="AI Health Assistant", page_icon="⚕️", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
#     ULTRA-PREMIUM CSS & ANIMATIONS 
# ==========================================
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] { display: none !important; }

    /* Smooth Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #090d16, #111827, #0f172a, #1e1e38);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Fade-In Effects for Text */
    .fade-in {
        animation: fadeIn 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Glowing Main Title */
    .main-title {
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        margin-top: 10vh;
        background: linear-gradient(135deg, #38bdf8 0%, #34d399 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 4px 15px rgba(56, 189, 248, 0.25));
        line-height: 1.15;
        letter-spacing: -1px;
    }

    .sub-title {
        font-size: 1.35rem;
        text-align: center;
        color: #94a3b8;
        margin-top: 20px;
        margin-bottom: 50px;
        font-weight: 400;
        line-height: 1.6;
    }

    /* GLASSMORPHISM - Secondary Buttons (Navbar & Footer) */
    button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    /* Secondary Button Hover Animation */
    button[kind="secondary"]:hover {
        background: rgba(56, 189, 248, 0.1) !important;
        color: #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15) !important;
    }

    /* HIGH-IMPACT PRIMARY BUTTON (Start Diagnosis) */
    button[kind="primary"] {
        background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%) !important;
        color: #0f172a !important;
        border-radius: 50px !important;
        padding: 14px 32px !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    /* Primary Button Hover Animation */
    button[kind="primary"]:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5) !important;
    }
    button[kind="primary"]:active {
        transform: translateY(-1px) scale(0.99) !important;
    }

    /* Clean Footer */
    hr {
        border-color: rgba(255, 255, 255, 0.05) !important;
        margin-top: 60px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
#         TOP NAVIGATION BAR
# ==========================================
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])

with c1:
    st.markdown("<h3 style='color: #38bdf8; font-weight: 800; margin-top:5px;'>🩺 Health AI</h3>", unsafe_allow_html=True)

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

st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 15px;'>© 2026 AI Health Assistant</p>", unsafe_allow_html=True)
