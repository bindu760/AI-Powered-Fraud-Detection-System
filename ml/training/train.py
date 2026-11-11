"""Train a reproducible demo model or train from a labeled CSV."""
from __future__ import annotations
import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml.evaluation.metrics import evaluate_predictions
from ml.preprocessing.features import FEATURES

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "fraud_model.joblib"

def demo_data(rows: int = 6000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    amount = rng.lognormal(3.3, 1.15, rows).clip(1, 20000)
    hour = rng.integers(0, 24, rows)
    day = rng.integers(0, 7, rows)
    international = rng.binomial(1, .12, rows)
    merchant_risk = rng.beta(2, 5, rows)
    velocity = rng.poisson(1.8, rows)
    score = -5.0 + .00018 * amount + .95 * international + 2.3 * merchant_risk + .28 * velocity + .8 * np.isin(hour, [0, 1, 2, 3, 4])
    probability = 1 / (1 + np.exp(-score))
    fraud = rng.binomial(1, probability)
    frame = pd.DataFrame(dict(amount=amount, hour=hour, day_of_week=day, is_international=international, merchant_risk=merchant_risk, velocity_1h=velocity, is_fraud=fraud))
    # Ensure a usable positive class for every deterministic demo seed.
    if frame.is_fraud.sum() < 10:
        frame.loc[frame.nlargest(20, "amount").index, "is_fraud"] = 1
    return frame

def train(csv_path: str | None = None, model_path: str | Path = MODEL_PATH) -> dict:
    frame = pd.read_csv(csv_path) if csv_path else demo_data()
    missing = set(FEATURES + ["is_fraud"]) - set(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
    frame = frame[FEATURES + ["is_fraud"]].dropna()
    if frame.is_fraud.nunique() < 2:
        raise ValueError("Training data must contain both fraud and legitimate examples")
    if not set(frame.is_fraud.unique()).issubset({0, 1}):
        raise ValueError("is_fraud must use only 0 (legitimate) and 1 (fraud)")
    values = frame[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Feature columns must contain finite numeric values")
    if (frame.amount <= 0).any() or (frame.velocity_1h < 0).any():
        raise ValueError("amount must be positive and velocity_1h cannot be negative")
    if not frame.hour.between(0, 23).all() or not frame.day_of_week.between(0, 6).all():
        raise ValueError("hour must be 0-23 and day_of_week must be 0-6")
    if not frame.is_international.isin([0, 1]).all() or not frame.merchant_risk.between(0, 1).all():
        raise ValueError("is_international must be 0/1 and merchant_risk must be between 0 and 1")
    X, y = frame[FEATURES], frame.is_fraud.astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=180, max_depth=12, min_samples_leaf=2, class_weight="balanced", random_state=42, n_jobs=-1))
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]
    destination = Path(model_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, destination)
    return {"model_path": str(destination), "rows": len(frame), "fraud_rate": float(y.mean()), **evaluate_predictions(y_test, probabilities)}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Labeled CSV containing model features and is_fraud")
    parser.add_argument("--model", default=str(MODEL_PATH))
    args = parser.parse_args()
    print(train(args.csv, args.model))

if __name__ == "__main__":
    main()
