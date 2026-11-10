# 🛡️ AI-Powered Fraud Detection System

An intelligent fraud detection system that uses Machine Learning to identify suspicious financial transactions, predict fraud probability, and explain model predictions using Explainable AI (SHAP).

## 🚀 Project Overview

Financial fraud is a major challenge in digital payment systems. This project aims to detect fraudulent transactions using Machine Learning algorithms and provide insights into suspicious transaction patterns.

The system analyzes transaction data, predicts the likelihood of fraud, and classifies transactions based on their risk levels.

## ✨ Key Features

- **Fraud Detection:** Identify fraudulent financial transactions using Machine Learning.
- **Fraud Probability:** Predict the probability of a transaction being fraudulent.
- **Risk Classification:** Categorize transactions into Low, Medium, and High Risk.
- **Explainable AI:** Use SHAP to understand why a transaction is classified as suspicious.
- **Transaction Monitoring:** Store and monitor transaction records.
- **Interactive Dashboard:** Visualize fraud statistics and transaction insights.
- **Model Evaluation:** Evaluate model performance using multiple classification metrics.

## 🧠 Machine Learning Algorithms

- Logistic Regression
- Random Forest
- XGBoost
- Isolation Forest (for anomaly detection)

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| Pandas & NumPy | Data Processing |
| Scikit-learn | Machine Learning |
| XGBoost | Fraud Classification |
| SHAP | Explainable AI |
| FastAPI | Backend API |
| PostgreSQL | Database |
| Streamlit | Dashboard |
| Plotly | Data Visualization |

## 🏗️ System Architecture

```text
Transaction Data
       |
       v
Data Preprocessing
       |
       v
Feature Engineering
       |
       v
Machine Learning Model
       |
       v
Fraud Probability
       |
       v
Risk Classification
       |
       v
SHAP Explainability
       |
       v
FastAPI Backend
       |
       v
PostgreSQL Database
       |
       v
Streamlit Dashboard
```

## 📊 Model Evaluation

The models will be evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- PR-AUC
- Confusion Matrix

Special attention will be given to fraud detection Recall and Precision because the dataset contains highly imbalanced classes.

## 📂 Project Structure

```text
ai-fraud-detection/
│
├── backend/
├── ml/
├── data/
├── dashboard/
├── models/
├── tests/
├── notebooks/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/bindu760/ai-fraud-detection.git
```

### 2. Navigate to the project

```bash
cd ai-fraud-detection
```

### 3. Create virtual environment

```bash
python -m venv .venv
```

### 4. Activate environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 📈 Project Status

🚧 Currently under development.

Planned milestones:

- [ ] Dataset collection and exploration
- [ ] Data preprocessing and feature engineering
- [ ] Machine Learning model training
- [ ] Model evaluation and comparison
- [ ] SHAP-based explainability
- [ ] FastAPI backend development
- [ ] PostgreSQL integration
- [ ] Streamlit dashboard
- [ ] Testing and deployment

## 🎯 Project Goal

To build an intelligent and explainable fraud detection system that demonstrates practical applications of Machine Learning, data analysis, backend development, and Explainable AI in financial security.

## 👩‍💻 Author

**Bindu Bhandari**

- GitHub: [@bindu760](https://github.com/bindu760)
- Email: bibh_csit2081@lict.edu.np

---

⭐ If you find this project interesting, consider giving it a star!