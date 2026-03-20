import streamlit as st
import pandas as pd
import plotly.express as px
from services.inference_service import analyze

# Simulated data for demo
import random
import datetime

def render():
    st.title("Crisis Dashboard")
    st.caption("Real-time analytics of mental health crisis trends")

    # ===== KPI CARDS =====
    col1, col2, col3, col4 = st.columns(4)

    total_analyses = random.randint(150, 500)
    high_risk = random.randint(10, 50)
    accuracy = round(random.uniform(85, 95), 2)
    status = "Operational"

    col1.metric("Total Analyses", total_analyses)
    col2.metric("High Risk Cases", high_risk)
    col3.metric("Accuracy", f"{accuracy}%")
    col4.metric("System Status", status)

    st.markdown("---")

    # ===== Crisis Trend (Line Chart) =====
    st.subheader("Crisis Trend")
    dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(10)][::-1]
    scores = [random.randint(10, 100) for _ in range(10)]
    trend_df = pd.DataFrame({"Date": dates, "Crisis Score": scores})
    fig = px.line(trend_df, x="Date", y="Crisis Score", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ===== Emotion Distribution (Pie Chart) =====
    st.subheader("Emotion Distribution")
    labels = ["Normal", "Stress", "Critical"]
    values = [random.randint(50, 200), random.randint(20, 100), random.randint(5, 50)]
    pie_df = pd.DataFrame({"Emotion": labels, "Count": values})
    pie_fig = px.pie(pie_df, names="Emotion", values="Count", color="Emotion",
                     color_discrete_map={"Normal":"lightblue", "Stress":"orange", "Critical":"red"})
    st.plotly_chart(pie_fig, use_container_width=True)