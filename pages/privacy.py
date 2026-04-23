import streamlit as st

st.set_page_config(page_title="Privacy", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e293b); color:white; }
.card { background: rgba(255,255,255,0.05); padding:30px; border-radius:20px; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([6,2])

with col1:
    st.markdown("## 🔒 Privacy Policy")

with col2:
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")

st.markdown('<div class="card">', unsafe_allow_html=True)

st.write("""
We respect your privacy.

- Your data is secure 🔐  
- We do not share personal info  
- Medical data is confidential  
- Used only for improving services  
""")

st.markdown('</div>', unsafe_allow_html=True)