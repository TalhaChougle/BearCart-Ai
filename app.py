import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import requests
from streamlit_lottie import st_lottie
from datetime import datetime
import random
import urllib.parse

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="BearCart Intelligence",
    layout="wide",
    page_icon="🐻"
)

# ==========================================
# GLOBAL STYLES
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;800&display=swap');

.stApp {
    background-color: #050511;
    color: #E0E0E0;
}

h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif;
    text-transform: uppercase;
    color: white;
}

p, div, label, span {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
}

section[data-testid="stSidebar"] {
    background-color: #020205;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOTTIE LOADER
# ==========================================
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_ecommerce = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_u4jjb9bd.json")
lottie_ai = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_m9zragkd.json")

# ==========================================
# DATA ENGINE
# ==========================================
@st.cache_data
def get_data(uploaded_file=None):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        np.random.seed(42)
        n = 1500
        df = pd.DataFrame({
            "session_id": range(n),
            "pages_viewed": np.random.randint(1, 10, n),
            "product_views": np.random.randint(0, 8, n),
            "add_to_cart": np.random.choice([0, 1, 2], n, p=[0.7, 0.2, 0.1]),
            "time_spent_sec": np.random.randint(10, 900, n),
            "device": np.random.choice(["Mobile", "Desktop"], n, p=[0.7, 0.3]),
            "location": np.random.choice(["Mumbai", "Delhi", "Bangalore"], n),
            "hour_of_day": np.random.randint(0, 23, n)
        })

    df["intent_score"] = (
        df["product_views"] * 2 +
        df["add_to_cart"] * 8 +
        df["time_spent_sec"] / 60 +
        df["pages_viewed"]
    )

    def segment(score):
        if score > 25:
            return "High Intent"
        elif score > 12:
            return "Medium Intent"
        return "Low Intent"

    df["segment"] = df["intent_score"].apply(segment)
    df["potential_revenue"] = df["segment"].apply(
        lambda x: random.randint(1000, 5000) if x == "High Intent" else 0
    )

    return df

# ==========================================
# SIDEBAR (FIXED INDENTATION)
# ==========================================
with st.sidebar:
    st.markdown("## 🐻 BearCart AI")
    st.markdown("---")

    menu = st.radio(
        "SYSTEM MODULES",
        ["🚀 Dashboard", "🧠 AI Analysis", "⚡ Action Center", "🔮 Future Lab"]
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        accept_multiple_files=False
    )

    if uploaded_file:
        df = get_data(uploaded_file)
        st.success("✅ Real data connected")
    else:
        df = get_data()
        st.info("ℹ️ Simulation mode")
# ==========================================
# DATA SAFETY CHECKS (IMPORTANT)
# ==========================================
if 'hour_of_day' not in df.columns:
    df['hour_of_day'] = np.random.randint(0, 24, len(df))

if 'session_id' not in df.columns:
    df['session_id'] = range(1, len(df) + 1)


# ==========================================
# DASHBOARD
# ==========================================
if menu == "🚀 Dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Traffic Intelligence — India")
        st.caption("Decoding clickstream into revenue signals")

    with col2:
        if lottie_ecommerce:
            st_lottie(lottie_ecommerce, height=100)

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("TOTAL SESSIONS", f"{len(df):,}")
    m2.metric("HIGH INTENT USERS", len(df[df["segment"] == "High Intent"]))
    m3.metric("REVENUE PIPELINE", f"₹{df['potential_revenue'].sum():,}")
    m4.metric("MOBILE SHARE", f"{(df['device'] == 'Mobile').mean() * 100:.1f}%")

    st.subheader("Hourly Traffic")
    trend = df.groupby("hour_of_day")["session_id"].count().reset_index()
    fig = px.area(trend, x="hour_of_day", y="session_id", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# AI ANALYSIS
# ==========================================
elif menu == "🧠 AI Analysis":
    st.title("Neural Insights")
    fig = px.scatter(
        df,
        x="time_spent_sec",
        y="product_views",
        color="segment",
        size="intent_score",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ACTION CENTER
# ==========================================
elif menu == "⚡ Action Center":
    st.title("Action Center")
    message = st.text_area(
        "WhatsApp Message",
        "Hi! Your items are almost sold out. Order now!"
    )

    if st.button("Launch WhatsApp"):
        encoded = urllib.parse.quote(message)
        st.markdown(
            f"[Open WhatsApp](https://wa.me/?text={encoded})",
            unsafe_allow_html=True
        )

# ==========================================
# FUTURE LAB
# ==========================================
elif menu == "🔮 Future Lab":
    st.title("Future Lab")
    if lottie_ai:
        st_lottie(lottie_ai, height=150)

    query = st.text_input("Ask the AI about your data")
    if query:
        st.success("AI Insight: Focus on High Intent Mobile Users 🚀")

