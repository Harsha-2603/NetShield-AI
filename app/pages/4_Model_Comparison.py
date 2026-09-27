import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="NetShield AI - Model Comparison",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# Title
# ==========================================

st.title("📊 Model Comparison")

st.write(
    "Recorded performance of the machine-learning models "
    "trained for NetShield AI."
)

st.info(
    "Note: the kernel models were trained using smaller "
    "training subsets than the full-data Logistic Regression "
    "and Linear SVM experiments."
)

# ==========================================
# Binary classification results
# ==========================================

binary_results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Linear SVM",
        "RBF SVM",
        "Polynomial SVM",
        "Bayesian Logistic Regression",
        "Custom Laplacian SVM"
    ],

    "Training Samples": [
        175341,
        175341,
        20000,
        20000,
        175341,
        5000
    ],

    "Accuracy": [
        0.8355,
        0.8300,
        0.8509,
        0.8392,
        0.8120,
        0.9404
    ],

    "Precision": [
        0.8019,
        0.8400,   # approximate from classification report
        0.8073,
        0.7847,
        0.7554,
        0.9910
    ],

    "Recall": [
        0.9313,
        0.8200,   # approximate from classification report
        0.9578,
        0.9757,
        0.9739,
        0.9475
    ],

    "F1": [
        0.8618,
        0.8200,   # approximate from classification report
        0.8761,
        0.8698,
        0.8508,
        0.9688
    ],

    "ROC-AUC": [
        0.9561,
        None,
        0.9559,
        0.9396,
        0.9562,
        0.9219
    ],

    "PR-AUC": [
        0.9668,
        None,
        0.9617,
        0.9189,
        0.9663,
        0.9976
    ]
})

# ==========================================
# Display table
# ==========================================

st.subheader("Binary Classification")

st.dataframe(
    binary_results,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# Accuracy chart
# ==========================================

st.subheader("Accuracy")

fig_accuracy = px.bar(
    binary_results,
    x="Model",
    y="Accuracy",
    title="Binary Model Accuracy"
)

st.plotly_chart(
    fig_accuracy,
    use_container_width=True
)

# ==========================================
# F1 chart
# ==========================================

st.subheader("F1 Score")

fig_f1 = px.bar(
    binary_results,
    x="Model",
    y="F1",
    title="Binary Model F1 Score"
)

st.plotly_chart(
    fig_f1,
    use_container_width=True
)

# ==========================================
# ROC-AUC / PR-AUC
# ==========================================

auc_results = binary_results.dropna(
    subset=["ROC-AUC", "PR-AUC"]
)

st.subheader("AUC Metrics")

auc_long = auc_results.melt(
    id_vars=["Model"],
    value_vars=["ROC-AUC", "PR-AUC"],
    var_name="Metric",
    value_name="Score"
)

fig_auc = px.bar(
    auc_long,
    x="Model",
    y="Score",
    color="Metric",
    barmode="group",
    title="ROC-AUC and PR-AUC"
)

st.plotly_chart(
    fig_auc,
    use_container_width=True
)

# ==========================================
# Regression results
# ==========================================

st.divider()

st.subheader("Regression Models")

regression_results = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Ridge Regression",
        "Huber Regression",
        "SVR",
        "Bayesian Linear Regression"
    ],

    "MAE": [
        5274.4156,
        5103.2254,
        3913.9204,
        19557.0044,
        5273.8416
    ],

    "RMSE": [
        15610.8257,
        15571.2343,
        22852.6097,
        230580.6537,
        15610.9363
    ],

    "R²": [
        0.9954,
        0.9954,
        0.9901,
        -0.0046,
        0.9954
    ],

    "Median AE": [
        3150.9380,
        2726.3161,
        233.2366,
        230.5847,
        3150.7310
    ]
})

st.dataframe(
    regression_results,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# Regression R²
# ==========================================

fig_r2 = px.bar(
    regression_results,
    x="Model",
    y="R²",
    title="Regression R²"
)

st.plotly_chart(
    fig_r2,
    use_container_width=True
)