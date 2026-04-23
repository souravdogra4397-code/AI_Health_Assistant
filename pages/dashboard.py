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

# ---------- ADVANCED CSS (Animations, Background, Cards, Buttons) ----------
st.markdown("""
<style>
/* Hide Default Sidebar Nav */
[data-testid="stSidebarNav"] {display:none;}

/* Beautiful Deep Premium Background */
.stApp {
    background: linear-gradient(135deg, #0b132b, #1c2541, #3a506b);
    color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar Styling & Menu Buttons */
section[data-testid="stSidebar"] {
    background: rgba(11, 19, 43, 0.85);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Make Radio Menu look like BIG Attractive Buttons */
div.stRadio > div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px 20px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
    width: 100%;
}
div.stRadio > div[role="radiogroup"] > label:hover {
    background: rgba(56, 189, 248, 0.15);
    border-color: #38bdf8;
    transform: translateX(5px);
}
/* Active Radio styling */
div.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] div {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}

/* Profile Icon Container */
.profile-box {
    text-align: center;
    padding: 20px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.1);
}
.profile-icon { font-size: 3rem; margin-bottom: 10px; }
.profile-name { font-size: 1.2rem; font-weight: bold; color: #38bdf8; }

/* Glassmorphism Cards with Hover Effects */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: all 0.4s ease;
}
.card:hover {
    transform: translateY(-5px);
    border-color: rgba(56,189,248,0.4);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
}

/* Header Animation */
@keyframes pulse {
    0% { transform: scale(1); filter: drop-shadow(0px 0px 10px rgba(56,189,248,0.5)); }
    50% { transform: scale(1.05); filter: drop-shadow(0px 0px 20px rgba(52,211,153,0.8)); }
    100% { transform: scale(1); filter: drop-shadow(0px 0px 10px rgba(56,189,248,0.5)); }
}
.main-header { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
.logo-animate { animation: pulse 3s infinite ease-in-out; }
.title {
    font-size: 2.8rem; font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;
}

/* Highly Attractive Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg, #38bdf8, #34d399) !important;
    color: #0b132b !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    border: none !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
}
button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.6) !important;
    transform: translateY(-3px) scale(1.02);
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

model_name = "llama-3.3-70b-versatile"

# ---------- AUTH CHECK ----------
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("⚠️ Please Login First.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/login.py")
    st.stop()

# ---------- MAIN HEADER ----------
st.markdown(f"""
    <div class='main-header'>
        <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="65" class="logo-animate">
        <h1 class='title'>AI Health Assistant</h1>
    </div>
    <p style="color: #94a3b8; font-size: 1.15rem; margin-bottom: 25px;">Your personal, secure, and intelligent medical workspace.</p>
""", unsafe_allow_html=True)
st.divider()

# ---------- SIDEBAR WITH PROFILE & MENU ----------
with st.sidebar:
    st.markdown(f"""
        <div class='profile-box'>
            <div class='profile-icon'>👨‍💻</div>
            <div class='profile-name'>Welcome, {st.session_state['username']}</div>
            <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 5px;">{datetime.date.today().strftime("%B %d, %Y")}</div>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navigation", [
        "💬 AI Chatbot",
        "🤒 Symptom Checker",
        "🧠 Risk Prediction",
        "📅 Appointment",
        "💊 Medicine Reminder",
        "🧾 Medical History"
    ], label_visibility="collapsed")
    
    st.write("\n" * 5) 
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # ✅ FIX: use_container_width=True ko hatakar width="stretch" kar diya
    if st.button("Logout 🚪", width="stretch"):
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

# ---------- SYMPTOM CHECKER (WITH HISTORY SAVE FIX) ----------
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
                            {"role": "system", "content": "You are a highly professional medical AI. Analyze the symptoms provided by the user. Give possible conditions and standard precautions."},
                            {"role": "user", "content": symptoms}
                        ]
                    )
                    ai_reply = res.choices[0].message.content
                    st.success("### Analysis Complete ✅")
                    st.write(ai_reply)
                    
                    # ✅ FIX: SAVE TO DATABASE FOR HISTORY TAB
                    try:
                        conn = create_connection()
                        cur = conn.cursor()
                        cur.execute("INSERT INTO history (username, symptoms, prediction) VALUES (?, ?, ?)", 
                                    (st.session_state['username'], symptoms, ai_reply))
                        conn.commit()
                        conn.close()
                    except Exception as db_err:
                        st.error(f"Failed to save history: {db_err}")
                        
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please enter your symptoms in the box above first.")
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- PREDICTION (LIFESTYLE & VITALS) ----------
elif menu == "🧠 Risk Prediction":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Cardiovascular Health Risk Prediction")
    st.write("Enter your basic details and lifestyle habits to calculate your estimated health risk score.")
    
    # Simple User Inputs (Lifestyle & Age)
    st.markdown("**👤 Basic Details & Lifestyle:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=25)
    with col2:
        smoke = st.selectbox("Smoking Habit", ["No, I don't smoke", "Occasionally", "Yes, regularly"])
    with col3:
        alcohol = st.selectbox("Alcohol Consumption", ["No, I don't drink", "Occasionally", "Yes, regularly"])

    st.write("")
    # Medical Vitals
    st.markdown("**🩺 Medical Vitals (Leave as is if you don't know):**")
    col4, col5 = st.columns(2)
    with col4:
        bp = st.slider("Blood Pressure (Normal is ~120)", min_value=80, max_value=200, value=120)
    with col5:
        sugar = st.slider("Fasting Sugar Level (Normal is ~99)", min_value=50, max_value=300, value=99)

    st.write("") 

    if st.button("Calculate My Risk", type="primary", use_container_width=True):
        st.markdown("<hr style='border-color: rgba(56,189,248,0.3);'>", unsafe_allow_html=True)
        
        # Risk Algorithm based on 5 new factors
        risk_score = 5 # Base score
        
        if age > 45: risk_score += 15
        if age > 60: risk_score += 10 # Extra age risk
        
        if smoke == "Occasionally": risk_score += 10
        elif smoke == "Yes, regularly": risk_score += 25
        
        if alcohol == "Occasionally": risk_score += 5
        elif alcohol == "Yes, regularly": risk_score += 15
        
        if bp > 130: risk_score += 15
        if bp > 150: risk_score += 15 # Severe BP risk
        
        if sugar > 100: risk_score += 15
        if sugar > 140: risk_score += 15 # Severe Sugar risk
        
        risk_score = min(risk_score, 100) # Cap at 100
        
        # Status Color
        if risk_score <= 30:
            status, color = "Low Risk - You are healthy! ✅", "#34d399"
        elif risk_score <= 60:
            status, color = "Moderate Risk - Monitor your lifestyle & diet. ⚠️", "#fbbf24"
        else:
            status, color = "High Risk - Please consult a doctor. 🚨", "#ef4444"

        # Results
        st.markdown(f"<h3 style='color: {color}; text-align: center;'>{status}</h3>", unsafe_allow_html=True)
        st.progress(risk_score / 100, text=f"Calculated Risk Score: {risk_score}%")
        
        st.write("")
        st.subheader("📊 Your Vitals vs Normal Targets")
        
        # Chart Data (Updated without BMI)
        chart_data = pd.DataFrame({
            "Metric": ["Blood Pressure", "Blood Pressure", "Sugar Level", "Sugar Level"],
            "Type": ["Your Level", "Healthy Normal", "Your Level", "Healthy Normal"],
            "Value": [bp, 120, sugar, 99]
        })
        
        df_pivot = chart_data.pivot(index="Metric", columns="Type", values="Value")
        st.bar_chart(df_pivot, height=350, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- APPOINTMENT ----------
elif menu == "📅 Appointment":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📅 Schedule a Doctor Visit")
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
    colM1, colM2 = st.columns(2)
    with colM1:
        med = st.text_input("Medicine Name (e.g., Paracetamol)")
    with colM2:
        time = st.time_input("Reminder Time")

    if st.button("Set Daily Reminder", type="primary"):
        if med:
            st.success(f"⏰ Alarm activated! We will remind you to take **{med}** at **{time.strftime('%I:%M %p')}**.")
        else:
            st.warning("Please enter the medicine name first.")
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- HISTORY (NOW WORKING & UPGRADED!) ----------
elif menu == "🧾 Medical History":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧾 Your Past Consultations")
    st.write("All your previous Symptom Checker analyses are securely saved here.")

    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT symptoms, prediction, date FROM history WHERE username=? ORDER BY date DESC", (st.session_state['username'],))
        data = cur.fetchall()
        conn.close()

        if data:
            # 1. Show record count
            st.success(f"✅ Found {len(data)} saved consultation(s).")
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=["Reported Symptoms", "AI Advice", "Date & Time"])
            
            # 2. Format Date and Time to look premium
            try:
                df['Date & Time'] = pd.to_datetime(df['Date & Time']).dt.strftime('%d %b %Y, %I:%M %p')
            except:
                pass # Agar date format pehle se string hai toh error ignore karega
            
            # Display Table
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.write("") # Spacer
            
            # 3. Add a Download CSV Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download History (CSV)",
                data=csv,
                file_name=f"health_history_{st.session_state['username']}.csv",
                mime="text/csv",
                type="primary"
            )
            
        else:
            st.info("📭 No historical data found. Try analyzing a symptom first!")

    except Exception as e:
        st.error(f"Database Connection Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: 50px; font-weight: 500; letter-spacing: 1px;'>© 2026 AI Health Assistant | Engineered by Sourav</p>", unsafe_allow_html=True)