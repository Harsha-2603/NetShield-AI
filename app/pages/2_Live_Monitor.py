import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="NetShield AI - Live Monitor",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# Load alert data
# ==========================================

ALERTS_PATH = "data/processed/alerts.csv"

alerts = pd.read_csv(ALERTS_PATH)

# ==========================================
# Page title
# ==========================================

st.title("🛡️ Live Traffic Monitor")

st.write(
    "Simulated network-flow replay using public test data."
)

st.info(
    "This is a controlled replay of dataset records, "
    "not live network traffic."
)

# ==========================================
# Controls
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    num_events = st.slider(
        "Number of flows",
        min_value=5,
        max_value=50,
        value=10
    )

with col2:
    delay = st.slider(
        "Delay between flows (seconds)",
        min_value=0.2,
        max_value=3.0,
        value=1.0,
        step=0.2
    )

with col3:
    start_button = st.button(
        "▶ Start Simulation"
    )

# ==========================================
# Simulation area
# ==========================================

simulation_placeholder = st.empty()

table_placeholder = st.empty()

# ==========================================
# Start simulation
# ==========================================

if start_button:

    recent_events = []

    events = alerts.head(num_events)

    for _, event in events.iterrows():

        # Current simulation timestamp
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Create event record
        current_event = {
            "Timestamp": timestamp,
            "Flow ID": int(event["flow_index"]),
            "Prediction": event["prediction"],
            "Attack Probability": (
                float(event["attack_probability"]) * 100
            ),
            "Attack Type": event["attack_type"],
            "Flow Bytes": int(event["flow_bytes"]),
            "Severity Score": float(event["severity_score"]),
            "Severity": event["severity"],
        }

        recent_events.append(current_event)

        # ----------------------------------
        # Display current event
        # ----------------------------------

        with simulation_placeholder.container():

            st.subheader(
                f"Flow {current_event['Flow ID']}"
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Prediction",
                current_event["Prediction"]
            )

            c2.metric(
                "Attack Probability",
                f"{current_event['Attack Probability']:.2f}%"
            )

            c3.metric(
                "Attack Type",
                current_event["Attack Type"]
            )

            c4.metric(
                "Severity",
                current_event["Severity"]
            )

            st.write(
                f"**Flow Bytes:** "
                f"{current_event['Flow Bytes']:,}"
            )

            st.write(
                f"**Severity Score:** "
                f"{current_event['Severity Score']:.2f}"
            )

            st.write(
                f"**Timestamp:** "
                f"{current_event['Timestamp']}"
            )

        # ----------------------------------
        # Update event table
        # ----------------------------------

        display_df = pd.DataFrame(recent_events)

        table_placeholder.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        time.sleep(delay)

    st.success("Simulation completed.")