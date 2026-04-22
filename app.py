# app.py
# Author: Bikram Singh
import streamlit as st
from database import create_tables

# Run DB setup on start
create_tables()

# initial_sidebar_state="collapsed" sidebar ko shuru se hi band rakhega
st.set_page_config(page_title="AI Health Assistant", page_icon="⚕️", layout="wide", initial_sidebar_state="collapsed")

# Naya Premium Modern Theme & Sidebar Hider
st.markdown("""
    <style>
    /* 1. COMPLETELY HIDE THE SIDEBAR & HEADER (Jo apne Red X mark kiya tha) */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }

    /* 2. NEW THEME: Deep Modern Tech Blue Background */
    .stApp {
        background: radial-gradient(circle at top, #111827, #030712);
        color: #e2e8f0;
    }
    
    /* 3. Main Title Styling - Cyan/Blue Gradient Text */
    .main-title {
        font-size: 4.5rem;
        font-weight: 800;
        text-align: center;
        margin-top: 10vh;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 4. Subtitle */
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #9ca3af;
        margin-bottom: 50px;
    }
    
    /* 5. PRIMARY BUTTON STYLING (Get Started) */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: white;
        border-radius: 30px;
        padding: 10px 20px;
        font-size: 1.3rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        box-shadow: 0px 0px 20px rgba(0, 242, 254, 0.4);
        transform: translateY(-2px);
    }

    /* 6. SECONDARY BUTTONS (Navbar & Footer) */
    button[kind="secondary"] {
        background-color: transparent;
        color: #9ca3af;
        border: 1px solid #374151;
        border-radius: 20px;
        transition: 0.3s;
    }
    button[kind="secondary"]:hover {
        border-color: #00f2fe;
        color: #00f2fe;
        background-color: rgba(0, 242, 254, 0.05);
    }
    
    /* Divider */
    hr {
        border-color: #1f2937;
        margin-top: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
with c1:
    st.markdown("<h3 style='color: white; padding-top: 5px;'>🩺💙📊 Health AI</h3>", unsafe_allow_html=True)
with c2:
    if st.button("About Us", use_container_width=True):
        st.toast("About Us section coming soon!") # Placeholder action
with c3:
    if st.button("Contact", use_container_width=True):
        st.toast("Contact functionality coming soon!")
with c4:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/login.py")  # Fixed path based on your VS Code
with c5:
    if st.button("Register", use_container_width=True):
        st.switch_page("pages/register.py") # Fixed path based on your VS Code

# --- MAIN HERO SECTION ---
st.markdown("<div class='main-title'>Next-Gen Healthcare,<br>Powered by AI.</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Instant symptom analysis. Smart disease prediction. Secure medical history.<br>Experience the future of personal health.</div>", unsafe_allow_html=True)

# --- CENTERED GET STARTED BUTTON ---
col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
with col_btn2:
    if st.button("🩺💙 Your Personalized Health Guide Start Your Diagnosis", type="primary", use_container_width=True):
        st.switch_page("pages/login.py")

# --- FOOTER & TERMS SECTION ---
st.markdown("<hr>", unsafe_allow_html=True)

# Footer Buttons Centered
f1, f2, f3, f4, f5 = st.columns([2, 1.5, 1.5, 2, 0.1])
with f2:
    if st.button("Privacy Policy", use_container_width=True):
        st.toast("Privacy Policy page will open here.")
with f3:
    if st.button("Terms & Conditions", use_container_width=True):
        st.toast("Terms & Conditions page will open here.")

# Copyright Text
st.markdown("<p style='text-align: center; color: #4b5563; font-size: 0.9rem; margin-top: 15px;'>© 2026 AI Health Assistant. All Rights Reserved.</p>", unsafe_allow_html=True)