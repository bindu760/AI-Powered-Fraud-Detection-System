"""SQLite-backed transaction persistence, with optional SQLAlchemy URL."""
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from backend.app.core.config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float)
    hour: Mapped[int] = mapped_column(Integer)
    day_of_week: Mapped[int] = mapped_column(Integer)
    is_international: Mapped[int] = mapped_column(Integer)
    merchant_risk: Mapped[float] = mapped_column(Float)
    velocity_1h: Mapped[float] = mapped_column(Float)
    fraud_probability: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(10))
    is_fraud: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

def initialize() -> None:
    Base.metadata.create_all(engine)

def save_transaction(data: dict) -> Transaction:
    with SessionLocal() as session:
        item = Transaction(**data)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

def list_transactions(limit: int = 100) -> list[Transaction]:
    with SessionLocal() as session:
        return list(session.scalars(select(Transaction).order_by(Transaction.id.desc()).limit(limit)))

def summary() -> dict:
    with SessionLocal() as session:
        total = session.scalar(select(func.count(Transaction.id))) or 0
        fraud = session.scalar(select(func.count(Transaction.id)).where(Transaction.is_fraud.is_(True))) or 0
        avg = session.scalar(select(func.avg(Transaction.fraud_probability))) or 0
        return {"total_transactions": total, "flagged_transactions": fraud, "fraud_rate": round(fraud / total, 4) if total else 0, "average_fraud_probability": round(float(avg), 4)}
