# app/pages/home.py

import streamlit as st
from services.inference_service import analyze
from services.voice_service import VoiceService
from services.language_service import translate_to_english, translate_to_hindi
from services.chatbot_service import get_response

voice = VoiceService()


def render():
    st.title("Antardhwani")
    st.caption("AI-powered mental health crisis detection system")
    st.markdown("")

    # Input section
    st.subheader("Text / Voice Input")
    col1, col2 = st.columns(2)

    with col1:
        user_input = st.text_area("Enter text", height=150, placeholder="Type something...")

    with col2:
        if st.button("Use Voice"):
            try:
                user_input = voice.listen()
                st.success(f"Captured: {user_input}")
            except:
                st.error("Voice input failed")

    analyze_btn = st.button("Analyze", use_container_width=True)

    if analyze_btn and user_input.strip():
        # Translate to English for model
        translated_text = translate_to_english(user_input)

        result = analyze(translated_text, user_id="user_1")

        st.markdown("---")

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Prediction", result.get("label", "N/A"))
        col2.metric("Crisis Score", result.get("score", 0))
        col3.metric("Risk Level", result.get("level", "N/A"))
        col4.metric("Confidence", f"{round(result.get('confidence',0)*100,2)}%")

        st.markdown("---")

        # Detected signals
        st.subheader("Detected Signals")
        keywords = result.get("keywords", [])
        if keywords:
            st.write(", ".join(keywords))
        else:
            st.write("No strong signals detected")

        st.markdown("---")

        # Behavior insights
        st.subheader("Behavior Insights")
        behavior = result.get("behavior", {})
        b1, b2 = st.columns(2)
        b1.write(f"Trend: {behavior.get('trend','N/A')}")
        b1.write(f"Repetition: {behavior.get('repetition','N/A')}")
        b2.write(f"Late Night Activity: {behavior.get('late_night','N/A')}")
        b2.write(f"Escalation: {behavior.get('escalation','N/A')}")

        st.markdown("---")

        # Geo Insight
        st.subheader("Geo Insight")
        st.write("Location:", result.get("location", "Not available"))

        # Alerts
        alerts = result.get("alerts", [])
        if alerts:
            st.markdown("---")
            st.subheader("System Alerts")
            for alert in alerts:
                st.error(alert)

        # Hindi translation
        st.markdown("---")
        st.subheader("Translated (Hindi)")
        try:
            hindi_text = translate_to_hindi(user_input)
            st.write(hindi_text)
        except:
            st.write("Translation not available")

    # Chatbot
    st.markdown("---")
    st.subheader("AI Support Chatbot")
    chat_input = st.text_input("Talk to AI")
    if chat_input:
        response = get_response(chat_input)
        st.write("Bot:", response)