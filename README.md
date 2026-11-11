# AI-Powered Fraud Detection System

A runnable learning/demo project with a scikit-learn fraud classifier, FastAPI prediction API, SQLite transaction history, and Streamlit dashboard. On the first prediction the API trains and saves a deterministic demonstration model automatically, so an external dataset or database is not needed to get started.

> This is a demonstration project. The synthetic training data and model are not suitable for real payment decisions.

## Requirements

- Python 3.11 (recommended) or 3.12
- pip

Python 3.13+ may not have compatible wheels for the pinned scientific packages. PostgreSQL is optional; SQLite is the default.

## Run locally (Windows PowerShell)

From this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs. In another terminal, activate the same environment and run:

```powershell
streamlit run dashboard/app.py
```

The dashboard is at `http://localhost:8501`. It uses the API at `http://127.0.0.1:8000` by default. The first prediction trains `models/fraud_model.joblib`; transaction records are saved in `data/fraud.db`.

## API

- `GET /health` — process health
- `GET /api/summary` — transaction and fraud-score aggregates
- `GET /api/transactions?limit=100` — latest saved records
- `POST /api/predict` — score and persist a transaction

Example request:

```json
{
  "amount": 850.0,
  "hour": 2,
  "day_of_week": 5,
  "is_international": 1,
  "merchant_risk": 0.8,
  "velocity_1h": 6
}
```

`day_of_week` is Monday=0 through Sunday=6. Risk levels are low (<35%), medium (35–69.9%), and high (70%+); `is_fraud` is true at a model probability of 50% or more.

## Train with your own labeled CSV

CSV must contain these columns: `amount,hour,day_of_week,is_international,merchant_risk,velocity_1h,is_fraud`. `is_fraud` must be 0/1 and include both classes. Train and save a model:

```powershell
python -m ml.training.train --csv data/raw/transactions.csv
```

The output is `models/fraud_model.joblib`. The API will use it on its next start/request. To select a custom model or database URL, set `MODEL_PATH` or `DATABASE_URL` in `.env` before starting the API. Example optional PostgreSQL URL: `postgresql+psycopg2://user:password@localhost:5432/fraud`.

## Project layout

- `ml/` — feature validation, model training, and prediction
- `backend/` — FastAPI routes, Pydantic schemas, SQLAlchemy persistence
- `dashboard/` — Streamlit prediction form and analytics
- `data/` — local database and optional datasets
- `models/` — generated model artifact

Generated model/database artifacts are ignored by git. See `.env.example` for supported settings.
