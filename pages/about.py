import streamlit as st

st.set_page_config(page_title="About", layout="wide")

# ===== CSS (same theme) =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    margin-top: 20px;
}

.topbar {
    display:flex;
    justify-content: space-between;
    align-items:center;
}
</style>
""", unsafe_allow_html=True)

# ===== TOP BAR =====
col1, col2 = st.columns([6,2])

with col1:
    st.markdown("## ℹ️ About AI Health Assistant")

with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

# ===== CONTENT =====
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🏥 AI Medical App (Project Idea)")
st.write("AI-based healthcare assistant that helps users:")

st.write("""
- Check symptoms 🤒  
- Predict diseases 🧠  
- Get health advice 💊  
- Book doctor appointments 📅  
""")

st.markdown('</div>', unsafe_allow_html=True)