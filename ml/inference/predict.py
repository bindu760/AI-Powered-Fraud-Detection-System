"""Load the persisted classifier and return human-readable risk."""
from pathlib import Path
import joblib
import pandas as pd
from ml.preprocessing.features import FEATURES, validate_transaction
from ml.training.train import MODEL_PATH, train

def predict(transaction: dict, model_path: str | Path = MODEL_PATH) -> dict:
    transaction = validate_transaction(transaction)
    path = Path(model_path)
    if not path.exists():
        train(model_path=path)
    bundle = joblib.load(path)
    probability = float(bundle["model"].predict_proba(pd.DataFrame([{k: transaction[k] for k in FEATURES}]))[0, 1])
    risk = "high" if probability >= .7 else "medium" if probability >= .35 else "low"
    return {"fraud_probability": round(probability, 6), "risk_level": risk, "is_fraud": probability >= .5}
