import streamlit as st
import sys
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random
import time

# ---- PATH SETUP ----
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    import pages.home as home
    import pages.live_feed as live_feed
    import pages.map as map_page
except ImportError:
    class DummyModule:
        def render(self):
            st.info("Page under construction")
    home = DummyModule()
    live_feed = DummyModule()
    map_page = DummyModule()

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Antardhwani AI | Crisis Detection Platform", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Initialize session state for continuous data
if 'crisis_data' not in st.session_state:
    st.session_state.crisis_data = {
        'suicide_risk': [random.randint(30, 70) for _ in range(30)],
        'substance_use': [random.randint(20, 60) for _ in range(30)],
        'mental_health': [random.randint(40, 80) for _ in range(30)],
        'timestamps': [(datetime.now() - timedelta(seconds=30-i)).strftime('%H:%M:%S') for i in range(30)]
    }
    st.session_state.alert_count = random.randint(8, 15)
    st.session_state.last_update = datetime.now()
    st.session_state.chat_open = False
    st.session_state.chat_messages = [
        {"role": "bot", "content": "👋 Hello! I'm your Antardhwani AI Assistant. How can I help you with crisis detection today?"}
    ]

# ---- ENHANCED CSS WITH HEALTH-APPROPRIATE COLORS ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;600;700&family=Quicksand:wght@300;400;600;700&display=swap');
    
    /* Global Styles - Health-appropriate colors */
    .stApp {
        background: linear-gradient(135deg, #0a1a2f 0%, #1a2f3f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Soft gradient overlay for health theme */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 30%, rgba(64, 224, 208, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, rgba(255, 182, 193, 0.05) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Header with soft medical gradient */
    .hero-header {
        background: linear-gradient(135deg, rgba(10, 26, 47, 0.95) 0%, rgba(26, 47, 63, 0.95) 100%);
        border: 1px solid rgba(64, 224, 208, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #40E0D0, #FFB6C1, #98D8C8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 0 20px rgba(64, 224, 208, 0.3);
    }
    
    .hero-tagline {
        font-size: 20px;
        color: #FFB6C1;
        margin: 5px 0 0 0;
        font-style: italic;
        font-family: 'Quicksand', sans-serif;
        font-weight: 300;
        text-shadow: 0 0 10px rgba(255, 182, 193, 0.3);
    }
    
    .live-badge {
        background: rgba(64, 224, 208, 0.15);
        border: 1px solid #40E0D0;
        border-radius: 20px;
        padding: 5px 15px;
        color: #40E0D0;
        font-size: 12px;
        display: inline-block;
        animation: pulse 2s ease infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; box-shadow: 0 0 10px #40E0D0; }
        100% { opacity: 0.8; }
    }
    
    /* KPI Cards with soft colors */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 15px;
        margin: 20px 0;
        position: relative;
        z-index: 10;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(10, 26, 47, 0.9), rgba(26, 47, 63, 0.9));
        border: 1px solid rgba(64, 224, 208, 0.2);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s;
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #40E0D0, #FFB6C1, #98D8C8);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #40E0D0;
        box-shadow: 0 10px 30px rgba(64, 224, 208, 0.2);
    }
    
    .kpi-icon { font-size: 28px; }
    .kpi-label { 
        color: rgba(255,255,255,0.7); 
        font-size: 12px;
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
    }
    .kpi-value { 
        font-family: 'Orbitron', sans-serif;
        font-size: 36px; 
        font-weight: 700;
        color: #40E0D0;
        margin: 5px 0;
        text-shadow: 0 0 10px rgba(64, 224, 208, 0.3);
    }
    
    /* Chart Containers */
    .chart-container {
        background: linear-gradient(135deg, rgba(10, 26, 47, 0.8), rgba(26, 47, 63, 0.8));
        border: 1px solid rgba(64, 224, 208, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(5px);
        position: relative;
        z-index: 10;
    }
    
    .chart-title {
        color: white;
        font-size: 18px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
    }
    
    .chart-badge {
        background: rgba(64, 224, 208, 0.15);
        border: 1px solid #40E0D0;
        border-radius: 15px;
        padding: 2px 10px;
        font-size: 11px;
        color: #40E0D0;
    }
    
    /* Map Container */
    .map-container {
        background: linear-gradient(135deg, rgba(10, 26, 47, 0.9), rgba(26, 47, 63, 0.9));
        border: 1px solid rgba(64, 224, 208, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(5px);
    }
    
    /* Navigation Buttons */
    .stButton > button {
        background: rgba(10, 26, 47, 0.8);
        border: 1px solid rgba(64, 224, 208, 0.3);
        color: #40E0D0;
        border-radius: 10px;
        padding: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        font-family: 'Quicksand', sans-serif;
        backdrop-filter: blur(5px);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #40E0D0, #FFB6C1);
        color: #0a1a2f;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(64, 224, 208, 0.3);
    }
    
    /* Chatbot Styles - Beautiful and prominent */
    .chatbot-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .chatbot-button {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #40E0D0, #FFB6C1);
        border: none;
        border-radius: 50%;
        color: white;
        font-size: 30px;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(64, 224, 208, 0.4);
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .chatbot-button:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 20px 40px rgba(64, 224, 208, 0.6);
    }
    
    .chatbot-button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        animation: rotate 3s linear infinite;
    }
    
    .chatbot-window {
        position: absolute;
        bottom: 90px;
        right: 0;
        width: 350px;
        background: linear-gradient(135deg, #0a1a2f, #1a2f3f);
        border: 2px solid rgba(64, 224, 208, 0.3);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
    }
    
    .chatbot-header {
        background: linear-gradient(135deg, #40E0D0, #FFB6C1);
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .chatbot-header h3 {
        margin: 0;
        font-family: 'Orbitron', sans-serif;
        color: #0a1a2f;
        font-size: 16px;
    }
    
    .chatbot-messages {
        height: 300px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(0,0,0,0.2);
    }
    
    .message {
        margin-bottom: 15px;
        animation: messageSlide 0.3s ease-out;
    }
    
    @keyframes messageSlide {
        from { transform: translateX(-10px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .bot-message {
        background: rgba(64, 224, 208, 0.15);
        border: 1px solid rgba(64, 224, 208, 0.3);
        border-radius: 15px 15px 15px 5px;
        padding: 12px 15px;
        max-width: 80%;
        color: white;
        font-family: 'Quicksand', sans-serif;
    }
    
    .user-message {
        background: rgba(255, 182, 193, 0.15);
        border: 1px solid rgba(255, 182, 193, 0.3);
        border-radius: 15px 15px 5px 15px;
        padding: 12px 15px;
        max-width: 80%;
        margin-left: auto;
        color: white;
        font-family: 'Quicksand', sans-serif;
    }
    
    .chatbot-input {
        display: flex;
        padding: 15px;
        background: rgba(0,0,0,0.3);
        gap: 10px;
        border-top: 1px solid rgba(64, 224, 208, 0.2);
    }
    
    .chatbot-input input {
        flex: 1;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(64, 224, 208, 0.3);
        border-radius: 10px;
        padding: 10px 15px;
        color: white;
        font-family: 'Quicksand', sans-serif;
    }
    
    .chatbot-input input:focus {
        outline: none;
        border-color: #40E0D0;
        box-shadow: 0 0 15px rgba(64, 224, 208, 0.3);
    }
    
    .chatbot-input button {
        background: linear-gradient(135deg, #40E0D0, #FFB6C1);
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        color: #0a1a2f;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-family: 'Quicksand', sans-serif;
    }
    
    .chatbot-input button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(64, 224, 208, 0.4);
    }
    
    .close-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        color: #0a1a2f;
        font-size: 20px;
        cursor: pointer;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }
    
    .close-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: rotate(90deg);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: rgba(255,255,255,0.3);
        font-size: 12px;
        border-top: 1px solid rgba(64, 224, 208, 0.1);
        margin-top: 30px;
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Continuous Update Indicator */
    .continuous-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #40E0D0;
        border-radius: 50%;
        margin-right: 5px;
        animation: continuousPulse 1s ease infinite;
    }
    
    @keyframes continuousPulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.5); }
        100% { opacity: 1; transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# ---- CHATBOT FUNCTIONS ----
def toggle_chat():
    st.session_state.chat_open = not st.session_state.chat_open

def add_message(role, content):
    st.session_state.chat_messages.append({"role": role, "content": content})

def get_bot_response(user_input):
    responses = {
        "hello": "👋 Hello! I'm here to help with mental health and crisis support. How are you feeling today?",
        "hi": "👋 Hi there! How can I assist you with crisis detection today?",
        "help": "🆘 I can help with:\n- Suicide prevention resources\n- Substance use support\n- Mental health guidance\n- Crisis hotlines\n- Emergency contacts",
        "suicide": "🚨 If you're having thoughts of suicide, please call the National Suicide Prevention Lifeline: **1-800-273-8255** or text HOME to **741741**. You matter and help is available 24/7.",
        "depression": "💙 Depression is treatable. Would you like me to share some coping strategies or connect you with mental health resources?",
        "anxiety": "😌 Anxiety can be overwhelming. Try deep breathing: inhale for 4 seconds, hold for 4, exhale for 4. Would you like more coping techniques?",
        "substance": "💊 Substance use support is available. SAMHSA National Helpline: **1-800-662-4357**. They offer free, confidential help 24/7.",
        "addiction": "🤝 Recovery is possible. Would you like information about treatment options or support groups?",
        "crisis": "🚑 If this is a medical emergency, please call **911** immediately. I can also connect you with crisis resources.",
        "emergency": "📞 Emergency contacts:\n• Police/Fire/Medical: **911**\n• Crisis Hotline: **988**\n• Suicide Lifeline: **1-800-273-8255**\n• SAMHSA: **1-800-662-4357**",
        "resources": "📚 Here are some resources:\n- NAMI Helpline: **1-800-950-6264**\n- Crisis Text Line: Text HOME to **741741**\n- Veterans Crisis Line: **1-800-273-8255** press 1",
        "thank": "💚 You're welcome! I'm here whenever you need support. Take care of yourself.",
        "bye": "👋 Take care! Remember, help is always available if you need it. Reach out anytime.",
        "default": "I'm here to support you. Could you tell me more about what you're experiencing? I can provide resources for suicide prevention, substance use, mental health, or crisis situations."
    }
    
    user_lower = user_input.lower()
    for key, response in responses.items():
        if key in user_lower:
            return response
    return responses["default"]

def render_chatbot():
    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
    
    if not st.session_state.chat_open:
        if st.button("💬", key="chat_btn", help="Open Crisis Support Chat"):
            st.session_state.chat_open = True
            st.rerun()
    else:
        st.markdown('<div class="chatbot-window">', unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div class="chatbot-header">
            <h3>🤖 Crisis Support Assistant</h3>
            <button class="close-btn" onclick="document.getElementById('close_chat').click()">✕</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Messages
        st.markdown('<div class="chatbot-messages">', unsafe_allow_html=True)
        for msg in st.session_state.chat_messages[-8:]:  # Show last 8 messages
            if msg["role"] == "bot":
                st.markdown(f'<div class="message"><div class="bot-message">🤖 {msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message"><div class="user-message">👤 {msg["content"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                user_input = st.text_input("", placeholder="Type your message...", label_visibility="collapsed", key="chat_input")
            with col2:
                submitted = st.form_submit_button("Send")
            
            if submitted and user_input:
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                response = get_bot_response(user_input)
                st.session_state.chat_messages.append({"role": "bot", "content": response})
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Close", key="close_chat", help="Close chat"):
            st.session_state.chat_open = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Function for continuous data update
def update_data_continuous():
    """Update data continuously for smooth graph movement"""
    # Generate new values with smooth transitions
    last_suicide = st.session_state.crisis_data['suicide_risk'][-1]
    last_substance = st.session_state.crisis_data['substance_use'][-1]
    last_mental = st.session_state.crisis_data['mental_health'][-1]
    
    # Add small random changes for smooth movement
    new_suicide = max(20, min(90, last_suicide + random.randint(-3, 3)))
    new_substance = max(15, min(85, last_substance + random.randint(-3, 3)))
    new_mental = max(30, min(95, last_mental + random.randint(-3, 3)))
    
    # Remove oldest, add newest
    st.session_state.crisis_data['suicide_risk'].pop(0)
    st.session_state.crisis_data['substance_use'].pop(0)
    st.session_state.crisis_data['mental_health'].pop(0)
    st.session_state.crisis_data['timestamps'].pop(0)
    
    st.session_state.crisis_data['suicide_risk'].append(new_suicide)
    st.session_state.crisis_data['substance_use'].append(new_substance)
    st.session_state.crisis_data['mental_health'].append(new_mental)
    st.session_state.crisis_data['timestamps'].append(datetime.now().strftime('%H:%M:%S'))
    
    # Update alert count occasionally
    if random.random() < 0.3:
        st.session_state.alert_count = max(5, min(25, st.session_state.alert_count + random.randint(-1, 2)))

# ---- HEADER ----
st.markdown(f"""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🧠 ANTARDHWANI AI</h1>
            <div class="hero-tagline">"Catching crises before they catch us."</div>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <div class="live-badge">
                <span class="continuous-indicator"></span>
                CONTINUOUS
            </div>
            <div style="color: #40E0D0;">{datetime.now().strftime('%H:%M:%S')}</div>
        </div>
    </div>
    <p style="color: rgba(255,255,255,0.5); margin-top: 10px; font-size: 14px;">
        AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use & Mental Health Crisis Detection
    </p>
</div>
""", unsafe_allow_html=True)

# ---- NAVIGATION ----
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"  # Start with Dashboard for continuous updates

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 HOME", key="nav_home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with col2:
    if st.button("📊 DASHBOARD", key="nav_dash", use_container_width=True):
        st.session_state.page = "Dashboard"
        st.rerun()

with col3:
    if st.button("🎥 LIVE FEED", key="nav_live", use_container_width=True):
        st.session_state.page = "Live"
        st.rerun()

with col4:
    if st.button("🗺️ MAP", key="nav_map", use_container_width=True):
        st.session_state.page = "Map"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ---- PAGE ROUTING ----
if st.session_state.page == "Home":
    home.render()

elif st.session_state.page == "Dashboard":
    # Update data continuously for smooth animation
    update_data_continuous()
    
    # ---- KPI CARDS ----
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    events_today = random.randint(25, 40)
    affected_areas = random.randint(5, 12)
    system_health = random.randint(95, 100)
    high_risk_zones = random.randint(3, 8)
    
    metrics = [
        {"icon": "🚨", "label": "ACTIVE ALERTS", "value": st.session_state.alert_count},
        {"icon": "📅", "label": "EVENTS TODAY", "value": events_today},
        {"icon": "📍", "label": "AFFECTED AREAS", "value": affected_areas},
        {"icon": "⚡", "label": "SYSTEM HEALTH", "value": f"{system_health}%"},
        {"icon": "⚠️", "label": "HIGH-RISK ZONES", "value": high_risk_zones}
    ]
    
    for i, metric in enumerate(metrics):
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{metric['icon']}</div>
            <div class="kpi-label">{metric['label']}</div>
            <div class="kpi-value">{metric['value']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- CHARTS WITH CONTINUOUS MOVEMENT ----
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-title">
            <span>📈 Continuous Crisis Detection Trends</span>
            <span class="chart-badge">LIVE STREAM</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Line chart with smooth movement
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=st.session_state.crisis_data['timestamps'],
            y=st.session_state.crisis_data['suicide_risk'],
            name="Suicide Risk",
            line=dict(color='#FF6B6B', width=3, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.1)',
            mode='lines',
            hovertemplate='<b>%{x}</b><br>Suicide Risk: %{y}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=st.session_state.crisis_data['timestamps'],
            y=st.session_state.crisis_data['substance_use'],
            name="Substance Use",
            line=dict(color='#FFD93D', width=3, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(255, 217, 61, 0.1)',
            mode='lines',
            hovertemplate='<b>%{x}</b><br>Substance Use: %{y}%<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=st.session_state.crisis_data['timestamps'],
            y=st.session_state.crisis_data['mental_health'],
            name="Mental Health",
            line=dict(color='#6BCB77', width=3, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(107, 203, 119, 0.1)',
            mode='lines',
            hovertemplate='<b>%{x}</b><br>Mental Health: %{y}%<extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=10, family='Quicksand'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                tickangle=45,
                tickfont=dict(size=8)
            ),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            height=350,
            margin=dict(l=30, r=30, t=40, b=30),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("""
        <div class="chart-title">
            <span>📊 Current Risk Scores</span>
            <span class="chart-badge">REAL-TIME</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Bar chart with current values
        current_values = [
            st.session_state.crisis_data['suicide_risk'][-1],
            st.session_state.crisis_data['substance_use'][-1],
            st.session_state.crisis_data['mental_health'][-1]
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Suicide Risk', 'Substance Use', 'Mental Health'],
            y=current_values,
            marker_color=['#FF6B6B', '#FFD93D', '#6BCB77'],
            text=[f"{v}%" for v in current_values],
            textposition='outside',
            textfont=dict(color='white', size=11),
            width=0.6
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=10, family='Quicksand'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
            height=350,
            margin=dict(l=30, r=30, t=30, b=30),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Language analysis with soft colors - FIXED VERSION
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-title">
        <span>🔤 Crisis Language Analysis</span>
        <span class="chart-badge">NLP</span>
    </div>
    """, unsafe_allow_html=True)
    
    keywords = {
        "suicide": random.randint(70, 95),
        "depression": random.randint(60, 90),
        "overdose": random.randint(50, 85),
        "help": random.randint(80, 98),
        "anxiety": random.randint(65, 88),
        "addiction": random.randint(55, 82),
        "trauma": random.randint(45, 75)
    }
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(keywords.values()),
        y=list(keywords.keys()),
        orientation='h',
        marker=dict(
            color=list(keywords.values()),
            colorscale='Teal',
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Frequency %",
                    font=dict(color='white', size=12)
                ),
                tickfont=dict(color='white', size=10)
            )
        ),
        text=[f"{v}%" for v in keywords.values()],
        textposition='outside',
        textfont=dict(color='white', size=10)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10, family='Quicksand'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        height=300,
        margin=dict(l=100, r=40, t=30, b=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh for continuous movement (500ms)
    time.sleep(0.5)
    st.rerun()

elif st.session_state.page == "Live":
    live_feed.render()

elif st.session_state.page == "Map":
    # Update data for map too
    update_data_continuous()
    
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-title">
        <span>🗺️ Crisis Map - Live Risk Assessment</span>
        <span class="chart-badge">CONTINUOUS</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Map with dynamic values
    m = folium.Map(
        location=[22.7196, 75.8577], 
        zoom_start=5,
        tiles='CartoDB dark_matter'
    )
    
    cities = [
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "type": "suicide", "risk": st.session_state.crisis_data['suicide_risk'][-1]/100},
        {"name": "Delhi", "lat": 28.6139, "lon": 77.2090, "type": "substance", "risk": st.session_state.crisis_data['substance_use'][-1]/100},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946, "type": "mental", "risk": st.session_state.crisis_data['mental_health'][-1]/100},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "type": "suicide", "risk": st.session_state.crisis_data['suicide_risk'][-1]/100},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639, "type": "substance", "risk": st.session_state.crisis_data['substance_use'][-1]/100},
        {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "type": "mental", "risk": st.session_state.crisis_data['mental_health'][-1]/100}
    ]
    
    for city in cities:
        if city["type"] == "suicide":
            color = "#FF6B6B"
        elif city["type"] == "substance":
            color = "#FFD93D"
        else:
            color = "#6BCB77"
        
        folium.CircleMarker(
            location=[city["lat"], city["lon"]],
            radius=8 + (city["risk"] * 15),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            popup=f"{city['name']}<br>Risk: {city['risk']*100:.0f}%<br>Type: {city['type']}",
            tooltip=f"{city['name']} - {city['risk']*100:.0f}%"
        ).add_to(m)
    
    st_folium(m, width=None, height=400, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh for map
    time.sleep(0.5)
    st.rerun()

# ---- CHATBOT ----
render_chatbot()

# ---- FOOTER ----
st.markdown(f"""
<div class="footer">
    <div style="margin-bottom: 5px;">🧠 "Catching crises before they catch us."</div>
    <div>Antardhwani AI | Mental Health & Crisis Detection Platform</div>
    <div style="margin-top: 5px;">© 2026 | 24/7 Crisis Support Available</div>
</div>
""", unsafe_allow_html=True)