import streamlit as st
st.set_page_config(page_title="SAFA: SPIRITUAL ASSISTANT FOR FAITH & AWARENESS", layout="wide")

from modules import sidebar
from tabs import home, daily_journaling, guided_zikir, daily_mindfulness, rekomendasi_hari_ini, dashboard

# ----------------- CSS -----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(to bottom right, #E8F5E9, #A5D6A7); color: #4E342E; }
.stButton>button { background-color: #2E7D32; color: white; font-weight: bold; border-radius: 8px; transition: all 0.2s ease; }
.stButton>button:hover { background-color: #1B5E20; }
[data-testid="stSidebar"] { background: linear-gradient(to bottom, #C8E6C9, #81C784); color: #4E342E; }
[data-testid="stSidebar"] .css-1d391kg { color: #4E342E; font-weight: bold; }
.stMarkdown, .stText, .stRadio, .stSelectbox, .stTextArea { color: #4E342E; }
</style>
""", unsafe_allow_html=True)

# Panggil sidebar
choice = sidebar.show_sidebar()

# Routing tab
if choice == "Home":
    home.show()
elif choice == "Daily Journaling":
    daily_journaling.show()
elif choice == "Guided Zikir":
    guided_zikir.show()
elif choice == "Daily Mindfulness Challenge":
    daily_mindfulness.show()
elif choice == "Rekomendasi Hari Ini":
    rekomendasi_hari_ini.show()
elif choice == "Dashboard":
    dashboard.show()
