import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.database import (
    initialize_database,
    get_reviews
)

initialize_database()

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="NetShield AI",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Load alerts
# -----------------------------

ALERTS_PATH = "data/processed/alerts.csv"

alerts = pd.read_csv(ALERTS_PATH)

# ==========================================
# LOAD ANALYST REVIEWS  
# ==========================================

reviews = get_reviews()

total_reviews = len(reviews)

confirmed_attacks = (
    reviews["status"] == "Confirmed Attack"
).sum()

false_positives = (
    reviews["status"] == "False Positive"
).sum()

needs_investigation = (
    reviews["status"] == "Needs Investigation"
).sum()

# -----------------------------
# Title
# -----------------------------

st.title("🛡️ NetShield AI")
st.subheader("Network Intrusion Detection Dashboard")

st.write(
    "ML-based network-flow analysis and decision-support system"
)

# -----------------------------
# Metrics
# -----------------------------

total_flows = len(alerts)

attack_count = (
    alerts["prediction"] == "Attack"
).sum()

benign_count = (
    alerts["prediction"] == "Benign"
).sum()

critical_count = (
    alerts["severity"] == "Critical"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Flows", total_flows)
col2.metric("Attacks", attack_count)
col3.metric("Benign", benign_count)
col4.metric("Critical Alerts", critical_count)

# Add a Review Summary section

st.divider()

st.subheader("Analyst Review Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Reviews",
        total_reviews
    )

with col2:
    st.metric(
        "Confirmed Attacks",
        confirmed_attacks
    )

with col3:
    st.metric(
        "False Positives",
        false_positives
    )

with col4:
    st.metric(
        "Needs Investigation",
        needs_investigation
    )
    
    
# ==========================================
# Alert Filters
# ==========================================

st.divider()

st.subheader("🔎 Alert Filters")

col1, col2, col3 = st.columns(3)

with col1:
    prediction_filter = st.selectbox(
        "Prediction",
        ["All", "Attack", "Benign"]
    )

with col2:
    severity_filter = st.multiselect(
        "Severity",
        sorted(alerts["severity"].dropna().unique()),
        default=sorted(alerts["severity"].dropna().unique())
    )

with col3:
    min_probability = st.slider(
        "Minimum Attack Probability (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

# ==========================================
# Apply filters
# ==========================================

filtered_alerts = alerts.copy()

if prediction_filter != "All":
    filtered_alerts = filtered_alerts[
        filtered_alerts["prediction"] == prediction_filter
    ]

filtered_alerts = filtered_alerts[
    filtered_alerts["severity"].isin(severity_filter)
]

filtered_alerts = filtered_alerts[
    filtered_alerts["attack_probability"] >= (
        min_probability / 100
    )
]

st.write(
    f"Showing **{len(filtered_alerts):,}** of "
    f"**{len(alerts):,}** alerts"
)

st.subheader("Filtered Alerts")

display_columns = [
    "flow_index",
    "prediction",
    "attack_probability",
    "attack_type",
    "severity"
]

st.dataframe(
    filtered_alerts[display_columns],
    use_container_width=True,
    hide_index=True
)

st.subheader("Investigate an Alert")

flow_ids = filtered_alerts["flow_index"].tolist()

if flow_ids:
    selected_flow = st.selectbox(
        "Select Flow ID",
        flow_ids
    )

    if st.button("Open Alert Investigation"):
        st.session_state["selected_flow_id"] = selected_flow
        st.switch_page("pages/3_Alert_Investigation.py")
else:
    st.info("No alerts match the current filters.")
    
# -----------------------------
# Attack distribution
# -----------------------------

st.divider()

st.subheader("Attack Type Distribution")

attack_data = (
    alerts[alerts["prediction"] == "Attack"]["attack_type"]
    .value_counts()
    .reset_index()
)

attack_data.columns = ["Attack Type", "Count"]

fig = px.bar(
    attack_data,
    x="Attack Type",
    y="Count",
    title="Detected Attack Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Recent alerts
# -----------------------------

st.subheader("Recent Alerts")

display_columns = [
    "flow_index",
    "prediction",
    "attack_probability",
    "attack_type",
    "flow_bytes",
    "severity_score",
    "severity"
]

st.dataframe(
    alerts[display_columns].head(20),
    use_container_width=True
)