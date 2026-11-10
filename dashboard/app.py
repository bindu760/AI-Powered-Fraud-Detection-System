"""Streamlit landing page for the fraud detection project."""

import streamlit as st

st.set_page_config(page_title="AI-Powered Fraud Detection System", page_icon="🛡️")
st.title("AI-Powered Fraud Detection System")
st.write(
    "A machine learning project for detecting potentially fraudulent "
    "financial transactions and explaining model predictions."
)
st.subheader("Development status")
st.info("Under development. No trained model or transaction analytics are available yet.")
st.subheader("Planned features")
st.markdown(
    """
    - Fraud probability and Low, Medium, or High risk classification
    - Model explanations using SHAP
    - Transaction storage with PostgreSQL
    - Prediction API built with FastAPI
    - Interactive fraud analytics dashboard
    """
)
