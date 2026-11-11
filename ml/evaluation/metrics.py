"""Evaluation helpers for imbalanced fraud classification."""
from __future__ import annotations

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

def evaluate_predictions(y_true, probabilities, threshold: float = 0.5) -> dict:
    """Return common binary-classification metrics and confusion matrix.

    PR-AUC (average precision) is included because fraud labels are usually
    highly imbalanced. ``probabilities`` must be the positive-class scores.
    """
    import numpy as np
    y_true = np.asarray(y_true, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    if y_true.ndim != 1 or probabilities.ndim != 1 or len(y_true) != len(probabilities):
        raise ValueError("y_true and probabilities must be one-dimensional arrays of equal length")
    if len(y_true) == 0 or not np.isin(y_true, [0, 1]).all():
        raise ValueError("y_true must contain at least one binary label")
    if not np.isfinite(probabilities).all() or ((probabilities < 0) | (probabilities > 1)).any():
        raise ValueError("probabilities must be finite values between 0 and 1")
    predicted = probabilities >= threshold
    result = {
        "accuracy": float(accuracy_score(y_true, predicted)),
        "precision": float(precision_score(y_true, predicted, zero_division=0)),
        "recall": float(recall_score(y_true, predicted, zero_division=0)),
        "f1": float(f1_score(y_true, predicted, zero_division=0)),
        "pr_auc": float(average_precision_score(y_true, probabilities)),
        "confusion_matrix": confusion_matrix(y_true, predicted, labels=[0, 1]).tolist(),
        "classification_report": classification_report(y_true, predicted, output_dict=True, zero_division=0),
    }
    result["roc_auc"] = float(roc_auc_score(y_true, probabilities)) if len(np.unique(y_true)) == 2 else None
    return result
