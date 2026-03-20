import streamlit as st
import time
from services.inference_service import analyze
import random

# Sample messages for simulation
messages = [
    "I feel like I can't handle anything anymore",
    "Just a normal day, nothing special",
    "I don't want to live anymore",
    "Feeling stressed with exams",
    "Everything is fine, happy today"
]

def render():
    st.title("Live Feed")
    st.caption("Simulated real-time user messages with risk levels")

    st.markdown("---")
    feed_container = st.empty()

    for i in range(10):
        message = random.choice(messages)
        result = analyze(message, user_id=f"user_{i}")
        risk = result["level"]
        color = "green" if risk=="Low" else "orange" if risk=="Medium" else "red"

        with feed_container.container():
            st.markdown(f"**User {i}:** {message}")
            st.markdown(f"**Risk Level:** <span style='color:{color}'>{risk}</span>", unsafe_allow_html=True)
            st.markdown("---")
        time.sleep(1)