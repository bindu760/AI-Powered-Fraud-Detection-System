"""Shared transaction feature definitions and validation."""
from __future__ import annotations
import math

FEATURES = ["amount", "hour", "day_of_week", "is_international", "merchant_risk", "velocity_1h"]

def validate_transaction(value: dict) -> dict:
    """Normalize and validate a transaction before inference or storage."""
    result = {key: value[key] for key in FEATURES}
    for key in ("amount", "merchant_risk", "velocity_1h"):
        result[key] = float(result[key])
    for key in ("hour", "day_of_week", "is_international"):
        result[key] = int(result[key])
    if not all(math.isfinite(result[key]) for key in ("amount", "merchant_risk", "velocity_1h")):
        raise ValueError("amount, merchant_risk, and velocity_1h must be finite numbers")
    if result["amount"] <= 0 or result["velocity_1h"] < 0:
        raise ValueError("amount must be positive and velocity_1h cannot be negative")
    if not 0 <= result["hour"] <= 23 or not 0 <= result["day_of_week"] <= 6:
        raise ValueError("hour must be 0-23 and day_of_week must be 0-6")
    if result["is_international"] not in (0, 1):
        raise ValueError("is_international must be 0 or 1")
    if not 0 <= result["merchant_risk"] <= 1:
        raise ValueError("merchant_risk must be between 0 and 1")
    return result
