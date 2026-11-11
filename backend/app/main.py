"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.api.endpoints.transactions import router
from backend.app.db.database import initialize

@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize()
    yield

app = FastAPI(title="AI Fraud Detection API", version="1.0.0", description="Demo fraud scoring and transaction analytics API", lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "AI Fraud Detection API", "docs": "/docs"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
