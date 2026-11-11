"""API request and response types."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TransactionInput(BaseModel):
    amount: float = Field(gt=0, le=1_000_000_000)
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6, description="Monday=0, Sunday=6")
    is_international: int = Field(ge=0, le=1)
    merchant_risk: float = Field(ge=0, le=1)
    velocity_1h: float = Field(ge=0, le=10_000)

class PredictionResponse(BaseModel):
    id: int
    fraud_probability: float
    risk_level: str
    is_fraud: bool

class TransactionResponse(PredictionResponse):
    model_config = ConfigDict(from_attributes=True)
    amount: float
    hour: int
    day_of_week: int
    is_international: int
    merchant_risk: float
    velocity_1h: float
    created_at: datetime

class SummaryResponse(BaseModel):
    total_transactions: int
    flagged_transactions: int
    fraud_rate: float
    average_fraud_probability: float
