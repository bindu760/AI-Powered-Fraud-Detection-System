# Data and training guide

Put your labeled CSV in `data/raw/` (the directory is excluded from git). Train from the project root:

```powershell
python -m ml.training.train --csv data/raw/transactions.csv
```

The required CSV columns and accepted values are:

| Column | Meaning | Expected values |
|---|---|---|
| `amount` | Transaction amount | Positive number |
| `hour` | Local transaction hour | Integer 0–23 |
| `day_of_week` | Day of week | Integer 0 Monday through 6 Sunday |
| `is_international` | Cross-border flag | 0 or 1 |
| `merchant_risk` | Merchant risk score | Number from 0 to 1 |
| `velocity_1h` | Transaction count in preceding hour | Nonnegative number |
| `is_fraud` | Ground truth label | 0 legitimate, 1 fraud; both labels required |

Training uses a stratified 80/20 split and a class-balanced Random Forest. It saves `models/fraud_model.joblib` and prints accuracy, precision, recall, F1, ROC-AUC, PR-AUC, confusion matrix, and class report. Keep the model and data together with the training code when moving deployments; joblib artifacts should only be loaded from trusted sources.
