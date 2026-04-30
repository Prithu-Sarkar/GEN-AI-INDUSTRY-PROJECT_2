"""
Database Service Module.
Persists investment reports via SQLAlchemy.
Falls back to local SQLite when Azure PostgreSQL is not configured.
"""
import os
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from src.shared.config import settings

Base = declarative_base()
SQLITE_PATH = (
    "/content/Multi-Agent Quantitative Analysis System/"
    "AAFA/crewai-agent-azure/outputs/reports.db"
)


class FinancialReport(Base):
    """ORM model for the reports_log table."""
    __tablename__ = "reports_log"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    ticker     = Column(String(10), nullable=False)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DatabaseService:
    """Wraps SQLAlchemy session management. Auto-selects Azure or SQLite."""

    def __init__(self):
        db_url = settings.azure_postgres_connection_string
        if db_url:
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            print("[DB] Connecting to Azure PostgreSQL")
        else:
            db_url = f"sqlite:///{SQLITE_PATH}"
            print(f"[DB] Using local SQLite: {SQLITE_PATH}")

        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def save_report(self, ticker: str, content: str) -> Optional[int]:
        """Persist a completed report. Returns the new record ID or None."""
        session = self.SessionLocal()
        try:
            rec = FinancialReport(ticker=ticker, content=content)
            session.add(rec)
            session.commit()
            print(f"[DB] Saved {ticker} report (ID: {rec.id})")
            return rec.id
        except Exception as e:
            print(f"[DB] Error: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    def fetch_reports(self, ticker: str = None) -> list:
        """Retrieve saved reports, optionally filtered by ticker."""
        session = self.SessionLocal()
        try:
            q = session.query(FinancialReport)
            if ticker:
                q = q.filter(FinancialReport.ticker == ticker.upper())
            return q.order_by(FinancialReport.created_at.desc()).all()
        except Exception as e:
            print(f"[DB] Fetch error: {e}")
            return []
        finally:
            session.close()