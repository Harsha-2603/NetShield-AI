import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import confusion_matrix

# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="NetShield AI - Attack Analytics",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# Load data
# ==========================================

ALERTS_PATH = "data/processed/alerts.csv"
TEST_PATH = "data/raw/UNSW_NB15_training-set.csv"

alerts = pd.read_csv(ALERTS_PATH)
test_data = pd.read_csv(TEST_PATH)

# ==========================================
# Title
# ==========================================

st.title("📈 Attack Analytics")

st.write(
    "Statistical analysis of detected network attacks, "
    "severity, probabilities, and traffic characteristics."
)

# ==========================================
# Summary metrics
# ==========================================

total_flows = len(alerts)

attack_count = (
    alerts["prediction"] == "Attack"
).sum()

benign_count = (
    alerts["prediction"] == "Benign"
).sum()

attack_rate = (
    attack_count / total_flows * 100
    if total_flows > 0 else 0
)

avg_probability = (
    alerts["attack_probability"].mean() * 100
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Flows",
    f"{total_flows:,}"
)

col2.metric(
    "Detected Attacks",
    f"{attack_count:,}"
)

col3.metric(
    "Detected Benign",
    f"{benign_count:,}"
)

col4.metric(
    "Attack Rate",
    f"{attack_rate:.2f}%"
)

# ==========================================
# Attack type distribution
# ==========================================

st.divider()

st.subheader("Attack Type Distribution")

attack_data = (
    alerts[
        alerts["prediction"] == "Attack"
    ]["attack_type"]
    .value_counts()
    .reset_index()
)

attack_data.columns = [
    "Attack Type",
    "Count"
]

fig_attack = px.bar(
    attack_data,
    x="Attack Type",
    y="Count",
    title="Detected Attack Categories"
)

st.plotly_chart(
    fig_attack,
    use_container_width=True
)

# ==========================================
# Severity distribution
# ==========================================

st.subheader("Severity Distribution")

severity_order = [
    "Informational",
    "Low",
    "High",
    "Critical"
]

severity_data = (
    alerts["severity"]
    .value_counts()
    .reindex(
        severity_order,
        fill_value=0
    )
    .reset_index()
)

severity_data.columns = [
    "Severity",
    "Count"
]

fig_severity = px.bar(
    severity_data,
    x="Severity",
    y="Count",
    title="Alert Severity Levels"
)

st.plotly_chart(
    fig_severity,
    use_container_width=True
)

# ==========================================
# Attack probability distribution
# ==========================================

st.subheader("Attack Probability Distribution")

fig_probability = px.histogram(
    alerts,
    x="attack_probability",
    nbins=30,
    title="Predicted Attack Probability"
)

fig_probability.update_xaxes(
    tickformat=".0%"
)

st.plotly_chart(
    fig_probability,
    use_container_width=True
)

st.write(
    f"Average predicted attack probability: "
    f"{avg_probability:.2f}%"
)

# ==========================================
# Flow-volume analysis
# ==========================================

st.subheader("Flow Volume Analysis")

flow_bytes = alerts["flow_bytes"]

volume_col1, volume_col2, volume_col3 = st.columns(3)

volume_col1.metric(
    "Average Flow Bytes",
    f"{flow_bytes.mean():,.2f}"
)

volume_col2.metric(
    "Median Flow Bytes",
    f"{flow_bytes.median():,.2f}"
)

volume_col3.metric(
    "Maximum Flow Bytes",
    f"{flow_bytes.max():,.0f}"
)

fig_volume = px.histogram(
    alerts,
    x="flow_bytes",
    nbins=40,
    title="Flow Byte Distribution"
)

st.plotly_chart(
    fig_volume,
    use_container_width=True
)

# ==========================================
# Attack probability vs flow volume
# ==========================================

st.subheader("Attack Probability vs Flow Volume")

fig_scatter = px.scatter(
    alerts.sample(
        min(10000, len(alerts)),
        random_state=42
    ),
    x="flow_bytes",
    y="attack_probability",
    color="severity",
    hover_data=[
        "prediction",
        "attack_type",
        "severity_score"
    ],
    title="Attack Probability vs Flow Bytes"
)

fig_scatter.update_yaxes(
    tickformat=".0%"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ==========================================
# Multiclass confusion matrix
# ==========================================

st.divider()

st.subheader("Multiclass Confusion Matrix")

eval_indices = alerts["flow_index"].astype(int)

true_classes = (
    test_data.iloc[eval_indices]["attack_cat"]
    .astype(str)
    .str.strip()
    .to_numpy()
)

predicted_classes = (
    alerts["attack_type"]
    .astype(str)
    .str.strip()
    .to_numpy()
)

# Explicit UNSW-NB15 categories
labels = [
    "Analysis",
    "Backdoor",
    "DoS",
    "Exploits",
    "Fuzzers",
    "Generic",
    "Normal",
    "Reconnaissance",
    "Shellcode",
    "Worms"
]

cm = confusion_matrix(
    true_classes,
    predicted_classes,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

fig_cm = px.imshow(
    cm_df,
    text_auto=True,
    aspect="auto",
    title="True Attack Category vs Predicted Attack Category"
)

fig_cm.update_xaxes(
    title="Predicted Category"
)

fig_cm.update_yaxes(
    title="True Category"
)

st.plotly_chart(
    fig_cm,
    use_container_width=True
)

# ==========================================
# Data table
# ==========================================

st.subheader("Attack Analytics Data")

st.dataframe(
    attack_data,
    use_container_width=True,
    hide_index=True
)
print("True classes:")
print(pd.Series(true_classes).value_counts())

print("\nPredicted classes:")
print(pd.Series(predicted_classes).value_counts())