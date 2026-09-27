import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# ==========================================
# Project root path
# ==========================================

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# ==========================================
# Database
# ==========================================

from src.database import (
    initialize_database,
    get_reviews
)

initialize_database()

# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="NetShield AI - Analyst Reviews",
    page_icon="📝",
    layout="wide"
)

# ==========================================
# Title
# ==========================================

st.title("📝 Analyst Reviews")

st.write(
    "Review and filter analyst decisions recorded for network-flow alerts."
)

# ==========================================
# Load reviews
# ==========================================

reviews = get_reviews()

# ==========================================
# Summary metrics
# ==========================================

total_reviews = len(reviews)

confirmed = (
    reviews["status"] == "Confirmed Attack"
).sum()

false_positive = (
    reviews["status"] == "False Positive"
).sum()

needs_investigation = (
    reviews["status"] == "Needs Investigation"
).sum()

benign = (
    reviews["status"] == "Benign"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Reviews",
    total_reviews
)

col2.metric(
    "Confirmed Attacks",
    confirmed
)

col3.metric(
    "False Positives",
    false_positive
)

col4.metric(
    "Needs Investigation",
    needs_investigation
)

# ==========================================
# Filter
# ==========================================

st.divider()

st.subheader("Filter Reviews")

status_options = [
    "All",
    "Needs Investigation",
    "Confirmed Attack",
    "False Positive",
    "Benign"
]

selected_status = st.selectbox(
    "Review Status",
    status_options
)

if selected_status != "All":
    filtered_reviews = reviews[
        reviews["status"] == selected_status
    ]
else:
    filtered_reviews = reviews

# ==========================================
# Display reviews
# ==========================================

st.subheader("Review History")

if filtered_reviews.empty:

    st.info(
        "No reviews match the selected filter."
    )

else:

    st.dataframe(
        filtered_reviews,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# Flow lookup
# ==========================================

st.divider()

st.subheader("Find Reviews by Flow ID")

flow_id = st.number_input(
    "Flow ID",
    min_value=0,
    step=1
)

flow_reviews = get_reviews(
    int(flow_id)
)

if flow_reviews.empty:

    st.info(
        f"No reviews recorded for Flow {int(flow_id)}."
    )

else:

    st.dataframe(
        flow_reviews,
        use_container_width=True,
        hide_index=True
    )