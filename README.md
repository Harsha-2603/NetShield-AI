# 🛡️ NetShield AI

### Network Intrusion Detection & Decision-Support System

NetShield AI is a machine-learning-based Network Intrusion Detection System (NIDS) that analyzes network-flow data, detects potential attacks, classifies attack categories, assigns severity levels, and provides an interactive dashboard for security analysts.

The system is designed around the **UNSW-NB15 dataset** and provides a controlled network-flow analysis and replay environment.

> **Note:** NetShield AI uses public dataset records for analysis and simulation. It does not capture or monitor live network traffic.

---

## 🚀 Features

### 1. Network Intrusion Detection
- Binary classification of network traffic into Attack and Benign.
- Attack probability score for each network flow.
- Severity assessment for detected alerts.

### 2. Attack Classification
The system classifies detected attacks into:
- Analysis
- Backdoor
- DoS
- Exploits
- Fuzzers
- Generic
- Reconnaissance
- Shellcode
- Worms
- Normal

### 3. Interactive Dashboard
The dashboard provides total flows, detected attacks, benign flows, critical alerts, attack-type distribution, severity distribution, attack-probability distribution, flow-volume analysis, and attack probability vs. flow volume.

### 4. Alert Filters
Analysts can filter alerts using prediction, severity, and minimum attack probability.

Example:
```text
Prediction: Attack
Severity: High
Minimum Attack Probability: 80%
```

### 5. Alert Investigation
Each alert can be investigated individually with prediction, attack probability, attack type, severity, severity score, flow bytes, and network-flow features.

### 6. Model Explanation
NetShield AI provides feature-level explanations using Logistic Regression, showing factors increasing and decreasing attack likelihood.

### 7. Analyst Feedback
Analysts can review alerts using:
- Needs Investigation
- Confirmed Attack
- False Positive
- Benign

Reviews are stored in SQLite.

### 8. Analyst Review History
The application provides total reviews, confirmed attacks, false positives, pending investigations, review history, filtering by status, and lookup by Flow ID.

### 9. Live Monitor
A controlled network-flow replay interface demonstrates alert generation using dataset records.

---

## 🤖 Machine Learning Models

### Binary Classification
- Logistic Regression
- Linear SVM
- RBF SVM
- Polynomial SVM
- Bayesian Logistic Regression
- Custom Laplacian SVM

### Regression Experiments
- Linear Regression
- Ridge Regression
- Huber Regression
- Bayesian Linear Regression
- Support Vector Regression

### Multiclass Classification
Attack categories include Analysis, Backdoor, DoS, Exploits, Fuzzers, Generic, Normal, Reconnaissance, Shellcode, and Worms.

---

## 📊 Binary Classification Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8355 | 0.8019 | 0.9313 | 0.8618 | 0.9561 | 0.9668 |
| Linear SVM | 0.8300 | 0.8400 | 0.8200 | 0.8200 | - | - |
| RBF SVM | 0.8509 | 0.8073 | 0.9578 | 0.8761 | 0.9559 | 0.9617 |
| Polynomial SVM | 0.8392 | 0.7847 | 0.9757 | 0.8698 | 0.9396 | 0.9189 |
| Bayesian Logistic Regression | 0.8120 | 0.7554 | 0.9739 | 0.8508 | 0.9562 | 0.9663 |
| Custom Laplacian SVM | 0.9404 | 0.9910 | 0.9475 | 0.9688 | 0.9219 | 0.9976 |

> Kernel-based models were evaluated using smaller training subsets than the full-data Logistic Regression and Linear SVM experiments.

---

## 📚 Dataset

### UNSW-NB15

The project uses training and testing data under:
```text
data/
├── raw/
│   ├── UNSW_NB15_training-set.csv
│   └── UNSW_NB15_testing-set.csv
└── processed/
    └── alerts.csv
```

The application uses an 82,332-row test set.

---

## 🏗️ Project Structure

```text
netshield-ai/
├── app/
│   ├── dashboard.py
│   └── pages/
│       ├── 2_Live_Monitor.py
│       ├── 3_Alert_Investigation.py
│       ├── 4_Model_Comparison.py
│       ├── 5_Attack_Analytics.py
│       └── 6_Analyst_Reviews.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── netshield.db
├── models/
├── notebooks/
├── src/
│   ├── __init__.py
│   └── database.py
├── tests/
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- **Programming:** Python
- **Machine Learning:** Scikit-learn, NumPy, SciPy, Joblib
- **Data Processing:** Pandas
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Application:** Streamlit
- **Database:** SQLite
- **Development:** VS Code, Jupyter / Google Colab, Git & GitHub

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/netshield-ai.git
cd netshield-ai
```

Replace `<your-username>` with your GitHub username.

### 2. Create a virtual environment

Windows:
```powershell
py -3.13 -m venv .venv313
```

Activate it:
```powershell
.\.venv313\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

The saved-model environment uses:
```text
scikit-learn==1.6.1
joblib==1.6.0
```

---

## ▶️ Run the Application

From the project root:

```powershell
python -m streamlit run app/dashboard.py
```

---

## 🔄 Application Workflow

```text
UNSW-NB15 Dataset
        ↓
Data Preprocessing
        ↓
Machine Learning Models
        ↓
Attack / Benign Prediction
        ↓
Attack Probability
        ↓
Attack Category
        ↓
Severity Assessment
        ↓
Alert Dashboard
        ↓
Alert Filtering
        ↓
Alert Investigation
        ↓
Model Explanation
        ↓
Analyst Review
        ↓
SQLite Database
        ↓
Review History & Dashboard Summary
```

---

## 🔍 Example Alert

```text
Flow ID            : 259
Prediction         : Attack
Attack Probability : 80.06%
Attack Type        : Shellcode
Severity            : High
Severity Score     : 65.45
Flow Bytes         : 168
```

---

## 🧠 Explainability

For Logistic Regression:
```text
Contribution = Processed Feature Value × Model Coefficient
```

Positive contributions push the model score toward the Attack class; negative contributions push it in the opposite direction.

---

## 💾 Analyst Review Persistence

Reviews are stored in:
```text
data/netshield.db
```

Each review records:
```text
ID
Flow ID
Status
Comment
Created At
```

---

## ⚠️ Limitations

- The system works with dataset records rather than live packet capture.
- Model performance depends on the UNSW-NB15 dataset.
- Some model experiments use smaller training subsets.
- Analyst review is a decision-support feature and does not automatically perform network remediation.

---

## 🔮 Future Improvements

- Real-time packet and flow ingestion
- Network sensor integration
- REST API backend
- Authentication and role-based access
- Alert prioritization
- Model retraining pipeline
- Additional explainability methods such as SHAP
- Cloud deployment
- Persistent multi-user analyst accounts
- Automated alert notification

---

## 📌 Project Status

**Current status:** Functional prototype

Implemented components include binary intrusion detection, multiclass attack classification, model comparison, attack analytics, alert filtering, alert investigation, model explanation, analyst feedback, SQLite persistence, review history, and controlled network-flow replay.

---

## 👨‍💻 Author

**Harsha Vardhan**  
B.Tech – Computer Science and Engineering

---

## 📄 License

This project is intended for educational and research purposes.
