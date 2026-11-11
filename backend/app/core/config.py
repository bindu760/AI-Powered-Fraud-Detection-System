"""Application settings loaded from environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env")
MODEL_PATH = Path(os.getenv("MODEL_PATH") or ROOT / "models" / "fraud_model.joblib")
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{ROOT.as_posix()}/data/fraud.db"
