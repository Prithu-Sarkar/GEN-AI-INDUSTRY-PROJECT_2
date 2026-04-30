"""
Streamlit Frontend.
Provides a web UI for the Financial Analyst Crew API.
Run with: streamlit run frontend/app.py
"""
import streamlit as st
import requests

st.set_page_config(page_title="AI Financial Analyst", layout="wide")
st.title("Multi-Agent Quantitative Analysis System")
st.markdown("Powered by CrewAI + Groq LLaMA 3.3")

ticker = st.text_input("Enter a stock ticker:", placeholder="e.g. NVDA, MSFT, AAPL").upper()

if st.button("Run Analysis") and ticker:
    with st.spinner(f"Analyzing {ticker}... this takes 2-5 minutes"):
        try:
            resp = requests.post(
                "http://localhost:8000/api/v1/analyze",
                json={"ticker": ticker},
                timeout=600
            )
            data = resp.json()
            if data.get("status") == "success":
                st.success(f"Analysis complete for {ticker}")
                st.markdown(data["report_content"])
                st.info(f"Report saved to: {data["report_url"]}")
            else:
                st.error(f"Error: {data}")
        except Exception as e:
            st.error(f"Request failed: {e}")