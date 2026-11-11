"""Streamlit dashboard for transaction scoring and saved analytics."""
import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Fraud Detection", page_icon="🛡️", layout="wide")
st.title("🛡️ AI Fraud Detection")
st.caption("Score a transaction and review the predictions saved by the API.")
api = st.sidebar.text_input("API URL", os.getenv("API_URL", "http://127.0.0.1:8000")).rstrip("/")

try:
    summary = requests.get(f"{api}/api/summary", timeout=3).json()
    records = requests.get(f"{api}/api/transactions", timeout=3).json()
except requests.RequestException:
    st.error("Cannot reach the API. Start it with `python -m uvicorn backend.app.main:app --reload`.")
    st.stop()

a, b, c, d = st.columns(4)
a.metric("Transactions", summary["total_transactions"])
b.metric("Flagged", summary["flagged_transactions"])
c.metric("Observed fraud rate", f"{summary['fraud_rate']:.1%}")
d.metric("Average model score", f"{summary['average_fraud_probability']:.1%}")

with st.expander("Score a transaction", expanded=True):
    with st.form("prediction"):
        left, right = st.columns(2)
        amount = left.number_input("Amount", min_value=0.01, value=250.0, step=25.0)
        hour = right.slider("Hour", 0, 23, 14)
        day = left.selectbox("Day of week", list(range(7)), format_func=lambda n: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][n])
        international = right.toggle("International transaction")
        merchant_risk = left.slider("Merchant risk", 0.0, 1.0, 0.2, 0.05)
        velocity = right.number_input("Transactions in previous hour", min_value=0, value=1)
        submitted = st.form_submit_button("Predict and save", type="primary")
    if submitted:
        body = {"amount": amount, "hour": hour, "day_of_week": day, "is_international": int(international), "merchant_risk": merchant_risk, "velocity_1h": velocity}
        try:
            result = requests.post(f"{api}/api/predict", json=body, timeout=30)
            result.raise_for_status()
            prediction = result.json()
            st.success(f"{prediction['risk_level'].upper()} risk · fraud probability {prediction['fraud_probability']:.1%} · record #{prediction['id']}")
            st.rerun()
        except requests.RequestException as exc:
            st.error(f"Prediction failed: {exc}")

st.subheader("Recent transactions")
if records:
    frame = pd.DataFrame(records)
    frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce")
    st.dataframe(frame[["id", "created_at", "amount", "fraud_probability", "risk_level", "is_fraud", "is_international"]], use_container_width=True, hide_index=True)
    st.subheader("Recent fraud probability scores")
    st.bar_chart(frame.set_index("id")[["fraud_probability"]], y="fraud_probability")
else:
    st.info("No predictions saved yet. Submit a transaction above to populate the dashboard.")
st.caption("Model uses generated demonstration data by default. Do not use its scores for real payment decisions.")
