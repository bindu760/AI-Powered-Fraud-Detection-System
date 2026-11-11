"""Application logic for scoring and recording a transaction."""
from backend.app.core.config import MODEL_PATH
from backend.app.db.database import save_transaction
from ml.inference.predict import predict

def score_and_save(transaction: dict):
    """Apply the model and persist its input and result as one record."""
    result = predict(transaction, MODEL_PATH)
    return save_transaction({**transaction, **result})
