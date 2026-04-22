# pages/dashboard.py
import streamlit as st
from openai import OpenAI
import os
import datetime
import pandas as pd
import numpy as np
from database import create_connection

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Health AI Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- ADVANCED CSS (Background, Sidebar, Cards) ----------
st.markdown("""
<style>
/* Hide Default Sidebar Nav */
[data-testid="stSidebarNav"] {display:none;}

/* Clean, Highly Visible Professional Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
}

/* Profile Icon Container */
.profile-box {
    text-align: center;
    padding: 20px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
.profile-icon {
    font-size: 3rem;
    margin-bottom: 10px;
}
.profile-name {
    font-size: 1.2rem;
    font-weight: bold;
    color: #38bdf8;
}

/* Glassmorphism Cards */
.card {
    background: rgba(255, 255, 255, 0.04);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(16px);
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Professional Header Title */
.main-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
}
.title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg, #38bdf8, #34d399) !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    border: none !important;
    transition: 0.3s;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.5) !important;
    transform: translateY(-2px);
}

/* Pin Logout to bottom of sidebar */
.logout-container {
    position: absolute;
    bottom: 20px;
    width: 85%;
    left: 50%;
    transform: translateX(-50%);
}
</style>
""", unsafe_allow_html=True)

# ---------- SAFE API KEY LOAD ----------
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ API Key not found! Add in secrets.toml or env variable")
    st.stop()

# ---------- GROQ CLIENT ----------
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# ✅ UPDATED MODEL (NO ERROR)
model_name = "llama-3.3-70b-versatile"

# ---------- AUTH CHECK ----------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Session expired. Please Login First.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/login.py")
    st.stop()

# ---------- MAIN HEADER ----------
st.markdown(f"""
    <div class='main-header'>
        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="60" style="filter: drop-shadow(0px 0px 10px rgba(56,189,248,0.5));">
        <h1 class='title'>AI Health Assistant</h1>
    </div>
    <p style="color: #94a3b8; font-size: 1.1rem;">Your personal, secure, and intelligent medical workspace.</p>
""", unsafe_allow_html=True)
st.divider()

# ---------- SIDEBAR WITH PROFILE & MENU ----------
with st.sidebar:
    # 1. Profile Box
    st.markdown(f"""
        <div class='profile-box'>
            <div class='profile-icon'>👨‍💻</div>
            <div class='profile-name'>Welcome, {st.session_state['username']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">{datetime.date.today().strftime("%B %d, %Y")}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📌 Main Menu")
    
    # 2. Reordered Menu (Chatbot & Prediction at top)
    menu = st.radio("Navigate Workspace", [
        "💬 AI Chatbot",
        "🤒 Symptom Checker",
        "🧠 Risk Prediction",
        "📅 Appointment",
        "💊 Medicine Reminder",
        "🧾 Medical History"
    ], label_visibility="collapsed")
    
    # 3. Logout Button pushed to bottom using whitespace/containers
    st.write("\n" * 10) 
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    if st.button("Logout 🚪", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")


# ==========================================
#              CORE FEATURES
# ==========================================

# ---------- CHATBOT ----------
if menu == "💬 AI Chatbot":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💬 Interactive Medical Assistant")
    st.write("Ask any health-related questions. Our AI will guide you instantly.")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("E.g., What are the best home remedies for a headache?")

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("AI is typing..."):
                try:
                    res = client.chat.completions.create(
                        model=model_name,
                        messages=st.session_state.chat
                    )
                    reply = res.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.chat.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"⚠️ Connection Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SYMPTOM CHECKER ----------
elif menu == "🤒 Symptom Checker":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤒 Smart Symptom Analyzer")
    st.write("Describe how you are feeling in simple English, and AI will provide possible conditions.")
    
    symptoms = st.text_area("How are you feeling today?", placeholder="Example: I have a severe headache, mild fever, and tiredness since yesterday.")

    if st.button("Analyze Symptoms", type="primary"):
        if symptoms:
            with st.spinner("Analyzing your symptoms using Llama 3 AI..."):
                try:
                    res = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "You are a highly professional medical AI. Analyze the symptoms provided by the user. Give possible conditions, standard precautions, and clearly state that this is an AI estimation and they should visit a real doctor."},
                            {"role": "user", "content": symptoms}
                        ]
                    )
                    st.info("### Analysis Complete ✅")
                    st.write(res.choices[0].message.content)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please enter your symptoms in the box above first.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- PREDICTION (ENHANCED WITH GRAPHS) ----------
elif menu == "🧠 Risk Prediction":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Cardiovascular Health Risk Prediction")
    st.write("Enter your vital signs below to see a comparative graph and calculate your estimated health risk score.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Your Age (Years)", min_value=1, max_value=120, value=25)
    with col2:
        bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=250, value=120)
    with col3:
        sugar = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=400, value=95)

    st.write("") # Spacer

    if st.button("Calculate Risk & View Graph", type="primary", use_container_width=True):
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 1. Basic Risk Algorithm
        risk_score = 10
        if age > 45: risk_score += 15
        if bp > 130: risk_score += 30
        if sugar > 100: risk_score += 25
        
        # 2. Status Determination
        if risk_score <= 30:
            status, color = "Low Risk - You are healthy! ✅", "green"
        elif risk_score <= 60:
            status, color = "Moderate Risk - Monitor your diet and exercise. ⚠️", "orange"
        else:
            status, color = "High Risk - Please consult a doctor. 🚨", "red"

        # 3. Results Display
        st.markdown(f"<h3 style='color: {color}; text-align: center;'>{status}</h3>", unsafe_allow_html=True)
        st.progress(risk_score / 100, text=f"Calculated Risk Score: {risk_score}%")
        
        st.write("")
        st.subheader("📊 Your Vitals vs Normal Levels")
        
        # 4. Comparative Bar Chart using Pandas
        chart_data = pd.DataFrame({
            "Metric": ["Blood Pressure", "Blood Pressure", "Glucose (Sugar)", "Glucose (Sugar)"],
            "Type": ["Your Level", "Healthy Target (Max)", "Your Level", "Healthy Target (Max)"],
            "Value": [bp, 120, sugar, 99]
        })
        
        # Pivot table for Streamlit Native Bar Chart
        df_pivot = chart_data.pivot(index="Metric", columns="Type", values="Value")
        st.bar_chart(df_pivot, height=350, use_container_width=True)

        st.info("💡 **Note:** This prediction model is a demonstration based on general thresholds and should not replace clinical diagnosis.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- APPOINTMENT ----------
elif menu == "📅 Appointment":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📅 Schedule a Doctor Visit")
    st.write("Select an available date to book an in-person or online consultation.")
    
    colA, colB = st.columns(2)
    with colA:
        doctor = st.selectbox("Select Specialist", ["General Physician", "Cardiologist", "Neurologist", "Dermatologist"])
    with colB:
        date = st.date_input("Select Date", min_value=datetime.date.today())

    if st.button("Confirm Booking", type="primary"):
        st.success(f"✅ Success! Your appointment with the {doctor} is booked for {date.strftime('%B %d, %Y')}.")
        st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- REMINDER ----------
elif menu == "💊 Medicine Reminder":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💊 Set Medicine Alarm")
    st.write("Never miss a dose. Enter your medicine details below.")

    colM1, colM2 = st.columns(2)
    with colM1:
        med = st.text_input("Medicine Name (e.g., Aspirin 500mg)")
    with colM2:
        time = st.time_input("Reminder Time")

    if st.button("Set Daily Reminder", type="primary"):
        if med:
            st.success(f"⏰ Alarm activated! We will remind you to take **{med}** at **{time.strftime('%I:%M %p')}**.")
        else:
            st.warning("Please enter the medicine name first.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- HISTORY ----------
elif menu == "🧾 Medical History":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧾 Your Past Consultations")
    st.write("Here are the records of your previous symptom analyses and predictions.")

    try:
        conn = create_connection()
        cur = conn.cursor()
        # Ensure the table name and columns match your database.py definitions exactly
        cur.execute("SELECT symptoms, prediction, date FROM history WHERE username=? ORDER BY date DESC", (st.session_state['username'],))
        data = cur.fetchall()
        conn.close()

        if data:
            # Convert to Pandas DataFrame for a clean, professional table display
            df = pd.DataFrame(data, columns=["Reported Symptoms", "AI Prediction / Advice", "Date & Time"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No past medical history found in the database.")

    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        st.write("Ensure your database setup allows fetching 'symptoms', 'prediction', and 'date'.")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #64748b; margin-top: 40px;'>© 2026 AI Health Assistant | Engineered by Sourav</p>", unsafe_allow_html=True)