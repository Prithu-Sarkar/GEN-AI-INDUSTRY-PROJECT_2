import warnings
warnings.filterwarnings("ignore")

import os
import streamlit as st
from src.core.planner import TravelPlanner
from src.utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("🌍 AI Travel Itinerary Planner")

with st.form("planner_form"):
    city      = st.text_input("📍 City")
    days      = st.slider("🗓️ Number of days", 1, 10, 3)
    interests = st.text_input("🎯 Interests (comma-separated)")
    style     = st.selectbox("💰 Travel Style", ["Budget", "Mid-range", "Luxury"])
    pace      = st.selectbox("🚶 Pace", ["Relaxed", "Balanced", "Packed"])
    month     = st.selectbox("📅 Month (optional)", ["Any","Jan","Feb","Mar","Apr",
                              "May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    submitted = st.form_submit_button("✨ Generate Itinerary")

if submitted:
    if city and interests:
        with st.spinner("🧠 Planning your trip..."):
            planner   = TravelPlanner()
            itinerary = planner.create_itinerary(
                city=city,
                days=days,
                interests=[i.strip() for i in interests.split(",")],
                style=style,
                pace=pace,
                month=None if month == "Any" else month
            )
        st.subheader("📄 Your Travel Plan")
        st.markdown(itinerary)
        logger.info("Response generated")
    else:
        st.warning("Please enter city and interests")