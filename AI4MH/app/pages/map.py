import streamlit as st
import pandas as pd
import pydeck as pdk
import random

def render():
    st.title("Crisis Map")
    st.caption("Geospatial visualization of crisis hotspots")

    # Simulated geo data
    data = pd.DataFrame({
        "lat": [28.7041 + random.uniform(-0.05, 0.05) for _ in range(20)],
        "lon": [77.1025 + random.uniform(-0.05, 0.05) for _ in range(20)],
        "risk": [random.choice(["Low", "Medium", "High"]) for _ in range(20)]
    })

    color_map = {"Low": [0,255,0], "Medium": [255,165,0], "High": [255,0,0]}
    data["color"] = data["risk"].map(color_map)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius=500,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=28.7041,
        longitude=77.1025,
        zoom=10,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Risk Level: {risk}"}
    )

    st.pydeck_chart(deck)