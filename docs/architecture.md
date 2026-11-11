# Architecture

The project has four runtime layers:

1. **Dashboard (`dashboard/app.py`)** collects a transaction and calls the HTTP API.
2. **API (`backend/app`)** validates the request, asks the service layer to score it, and returns the saved transaction.
3. **ML (`ml/`)** creates a deterministic demo dataset when needed, trains a Random Forest, persists it with joblib, and scores future transactions with the same feature order.
4. **Storage (`backend/app/db`)** keeps prediction input and output in SQLite by default. SQLAlchemy can use a PostgreSQL URL when configured.

The API creates the database tables on startup. It creates a demo model on the first call to `POST /api/predict` if the model file does not exist. This keeps first-time setup short, but model training adds several seconds to that first request.

## Prediction contract

Each request uses six numeric features: amount, hour, day of week, international flag, merchant risk, and transaction count in the previous hour. The response includes the model probability, risk band, binary decision, generated record ID, and timestamp. `is_fraud` uses a 0.50 probability threshold. Dashboard risk bands use low `<0.35`, medium `0.35–<0.70`, and high `>=0.70`.

The included synthetic data illustrates the software flow only. A production system needs representative labeled data, leakage review, calibrated thresholds, monitoring, access controls, and a human-reviewed decision process.
