"""Prediction, transaction history, and aggregate API routes."""
from fastapi import APIRouter, Query
from backend.app.db.database import list_transactions, summary
from backend.app.services.transactions import score_and_save
from backend.app.schemas.transaction import SummaryResponse, TransactionInput, TransactionResponse

router = APIRouter(prefix="/api", tags=["transactions"])

@router.post("/predict", response_model=TransactionResponse)
def create_prediction(payload: TransactionInput):
    transaction = payload.model_dump()
    return score_and_save(transaction)

@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(limit: int = Query(100, ge=1, le=500)):
    return list_transactions(limit)

@router.get("/summary", response_model=SummaryResponse)
def get_summary():
    return summary()
