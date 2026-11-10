"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="AI Fraud Detection API", version="1.0.0")


@app.get("/")
def root() -> dict[str, str]:
    """Return a basic API status message."""
    return {"status": "ok"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report that the API process is healthy."""
    return {"status": "healthy"}
