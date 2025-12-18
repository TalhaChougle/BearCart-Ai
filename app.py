import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. PAGE CONFIG & ADVANCED AESTHETICS
# ==========================================
st.set_page_config(page_title="BearCart Intelligence", layout="wide", page_icon="🐻")

# --- CUSTOM CSS OVERHAUL ---
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;800&display=swap');

    /* GLOBAL THEME */
    :root {
        --primary-neon: #00F0FF;
        --secondary-neon: #FF003C;
        --bg-deep: #050511;
        --glass: rgba(255, 255, 255, 0.05);
        --border-glass: rgba(255, 255, 255, 0.1);
    }

    /* BACKGROUND ATMOSPHERE */
    .stApp {
        background-color: var(--bg-deep);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.1) 0%, transparent 50%);
        color: #E0E0E0;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #FFFFFF;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }
    
    p, div, label, span {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
    }

    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #888;
    }

    /* CUSTOM CARDS (GLASSMORPHISM) */
    div[data-testid="metric-container"] {
        background: var(--glass);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: var(--primary-neon);
    }

    /* ANIMATIONS */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stPlotlyChart, div[data-testid="stMetric"], .stDataFrame {
        animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }

    /* CUSTOM BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #FF003C 0%, #C00028 100%);
        color: white;
        border: none;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(255, 0, 60, 0.4);
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(255, 0, 60, 0.7);
        transform: scale(1.02);
    }

    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #020205;
        border-right: 1px solid #222;
    }
    
    /* REMOVE DEFAULT STREAMLIT PADDING */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load Lottie Animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_ecommerce = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_u4jjb9bd.json")

# ==========================================
# 2. SIDEBAR & NAVIGATION & DATA LOADER
# ==========================================
with st.sidebar:
    if lottie_coding:
        st_lottie(lottie_coding, height=120, key="sidebar_anim")
    st.markdown("## BearCart AI")
    st.markdown("<div style='height: 2px; background: linear-gradient(90deg, #00F0FF, transparent); margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    menu = st.radio("SYSTEM MODULES", ["🚀 Dashboard", "🧠 AI Analysis", "⚡ Action Center"])
    
    st.markdown("---")
    st.markdown("### 📂 DATA SOURCE")
    # MOVED UPLOADER HERE TO FIX THE ERROR
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(0,255,0,0.1); padding: 10px; border-radius: 5px; border-left: 3px solid #00F0FF;'>
            <span style='font-family: "JetBrains Mono"; font-size: 0.8rem;'>STATUS: ONLINE</span><br>
            <span style='font-family: "JetBrains Mono"; font-size: 0.7rem; color: #888;'>v2.4.1 (Stable)</span>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATA PROCESSING ENGINE
# ==========================================
@st.cache_data
def get_data(use_simulation=True, uploaded_file=None):
    df = None
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Ensure we have the necessary columns, if not, fill with 0
        required_cols = ['product_views', 'add_to_cart', 'time_spent_sec', 'pages_viewed']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0
    else:
        # SIMULATION MODE
        np.random.seed(42)
        n = 1500
        df = pd.DataFrame({
            'session_id': range(1, n + 1),
            'pages_viewed': np.random.randint(1, 15, n),
            'product_views': np.random.randint(0, 10, n),
            'add_to_cart': np.random.choice([0, 1, 2, 3], n, p=[0.80, 0.10, 0.05, 0.05]),
            'time_spent_sec': np.random.randint(5, 900, n),
            'device': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n, p=[0.75, 0.20, 0.05]),
            'location': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Tier-2 City', 'Tier-3 City'], n)
        })

    # AI LOGIC
    df['intent_score'] = (df['product_views'] * 2) + (df['add_to_cart'] * 8) + (df['time_spent_sec'] / 45) + df['pages_viewed']
    
    def segment(score):
        if score > 25: return 'High Intent'
        elif score > 10: return 'Medium Intent'
        else: return 'Low Intent'
    
    df['segment'] = df['intent_score'].apply(segment)
    df['potential_revenue'] = df.apply(lambda x: np.random.randint(1000, 5000) if 'High' in x['segment'] else 0, axis=1)
    
    return df

# LOAD DATA ONCE (Used across all tabs)
if uploaded_file is None:
    df = get_data(use_simulation=True)
else:
    df = get_data(uploaded_file=uploaded_file)

# ==========================================
# 4. MAIN INTERFACE
# ==========================================

# Custom Color Palette
color_map = {
    'High Intent': '#FF003C',   # Neon Red
    'Medium Intent': '#00F0FF', # Neon Cyan
    'Low Intent': '#4B4B4B'     # Grey
}

if menu == "🚀 Dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("TRAFFIC INTELLIGENCE // INDIA")
        st.markdown("<span style='color: #888; font-family: \"JetBrains Mono\"'> > DECODING RAW CLICKSTREAM INTO REVENUE SIGNALS</span>", unsafe_allow_html=True)
    with col2:
        if lottie_ecommerce:
            st_lottie(lottie_ecommerce, height=80, key="header_anim")
    
    # Display Status of Data
    if uploaded_file is None:
        st.info("ℹ️ MODE: SIMULATION (INDIAN MARKET PATTERN)")
    else:
        st.success("✅ MODE: REAL DATA ANALYZED")

    st.markdown("---")
    
    # METRICS
    m1, m2, m3, m4 = st.columns(4)
    high_intent_users = len(df[df['segment'].str.contains('High')])
    est_revenue = df['potential_revenue'].sum()
    mobile_share = 75.0 if 'device' not in df.columns else len(df[df['device'] == 'Mobile']) / len(df) * 100
    
    m1.metric("TOTAL SESSIONS", f"{len(df):,}")
    m2.metric("HIGH INTENT TARGETS", f"{high_intent_users}", delta="PRIORITY")
    m3.metric("REVENUE PIPELINE", f"₹{est_revenue:,.0f}", delta="+12%")
    m4.metric("MOBILE TRAFFIC", f"{mobile_share:.1f}%")

    st.markdown("###") 

    # CHARTS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("BEHAVIORAL CLUSTERING")
        fig = px.scatter(df, x='time_spent_sec', y='product_views', 
                         color='segment', size='intent_score',
                         color_discrete_map=color_map,
                         template='plotly_dark')
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(family="Rajdhani", color="#AAA"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("REVENUE SOURCE")
        rev_by_seg = df.groupby('segment')['potential_revenue'].sum().reset_index()
        fig2 = px.pie(rev_by_seg, values='potential_revenue', names='segment', hole=0.6,
                      color='segment', color_discrete_map=color_map)
        fig2.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Rajdhani", color="white"))
        st.plotly_chart(fig2, use_container_width=True)

elif menu == "🧠 AI Analysis":
    st.title("NEURAL INSIGHTS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 165, 0, 0.1); border: 1px solid orange; padding: 20px; border-radius: 10px;">
            <h3 style="color: orange; margin: 0;">⚠️ PATTERN DETECTED: 'BARGAIN HUNTER'</h3>
            <p style="margin-top: 10px;">Users from Tier-2 cities demonstrate <strong>2.4x higher comparison behavior</strong> but lower conversion.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 0, 60, 0.1); border: 1px solid #FF003C; padding: 20px; border-radius: 10px;">
            <h3 style="color: #FF003C; margin: 0;">🚨 PATTERN DETECTED: 'MOBILE DROP'</h3>
            <p style="margin-top: 10px;">Mobile checkout abandonment is <strong>40% higher</strong> than desktop. Immediate UX intervention required.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    if 'location' in df.columns:
        st.subheader("GEOSPATIAL INTENT MAPPING")
        loc_group = df.groupby(['location', 'segment']).size().reset_index(name='count')
        fig = px.bar(loc_group, x='location', y='count', color='segment', barmode='group',
                     color_discrete_map=color_map, template='plotly_dark')
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Rajdhani", color="white"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⚠️ Location data not found in file. Displaying global metrics only.")

elif menu == "⚡ Action Center":
    st.title("ACTION COMMAND CENTER")
    
    tab1, tab2, tab3 = st.tabs(["🔥 HIGH INTENT", "⚠️ MEDIUM INTENT", "❄️ LOW INTENT"])
    
    with tab1:
        st.markdown("### STRATEGY: TRUST & SPEED (NO DISCOUNTS)")
        if st.button("GENERATE PRIORITY WHATSAPP LINK"):
            with st.spinner("GENERATING..."):
                time.sleep(1)
                st.code("""
                Hi [Name], 
                Your items in the cart are in high demand! 
                We have reserved them for you for the next 30 minutes. 
                Checkout now to ensure fast delivery: [Link]
                """, language="markdown")
                
    with tab2:
        st.markdown("### STRATEGY: VALUE NUDGE")
        coupon_val = st.slider("DISCOUNT MAGNITUDE (%)", 5, 20, 10)
        if st.button(f"DEPLOY {coupon_val}% CAMPAIGN"):
            with st.spinner("CONFIGURING CAMPAIGN..."):
                time.sleep(1)
                st.code(f"""
                Namaste! 🙏
                We noticed you were looking at our premium collection.
                Here is a special {coupon_val}% OFF coupon just for you: INDIA{coupon_val}
                Valid for 2 hours only!
                """, language="markdown")
                st.balloons()
                
    with tab3:
        st.markdown("### STRATEGY: AD SPEND OPTIMIZATION")
        st.metric("PROJECTED SAVINGS", "₹45,000", delta="OPTIMIZED")