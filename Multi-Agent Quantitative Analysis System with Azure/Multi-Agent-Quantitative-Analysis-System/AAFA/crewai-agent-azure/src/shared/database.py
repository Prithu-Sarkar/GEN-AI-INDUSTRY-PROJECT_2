"""
Database Service Module.

Handles persistence of investment reports via SQLAlchemy ORM.
In Colab (no Azure): automatically falls back to a local SQLite database
so the pipeline never fails due to missing cloud credentials.

Table schema:
    reports_log (id, ticker, content, created_at)
"""

import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional # Moved to top
from src.shared.config import settings

# SQLAlchemy declarative base — all ORM models inherit from this
Base = declarative_base()


class FinancialReport(Base):
    """
    ORM model mapping to the reports_log table.

    Columns:
        id (int): Auto-incremented primary key.
        ticker (str): Stock symbol (max 10 chars).
        content (Text): Full Markdown report text.
        created_at (DateTime): UTC timestamp of insertion.
    """
    __tablename__ = 'reports_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DatabaseService:
    """
    Service class wrapping SQLAlchemy session management.

    Automatically selects the correct DB URL:
      - Azure PostgreSQL if configured.
      - Local SQLite (outputs/reports.db) as fallback for Colab.
    """

    def __init__(self):
        # Determine database URL
        db_url = settings.azure_postgres_connection_string

        if db_url:
            # Normalize old "postgres://" prefix to "postgresql://"
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            print('[DB] Connecting to Azure PostgreSQL')
        else:
            # Colab fallback: lightweight SQLite file in the outputs directory
            sqlite_path = '/content/Multi-Agent Quantitative Analysis System/AAFA/crewai-agent-azure/outputs/reports.db'
            db_url = f'sqlite:///{sqlite_path}'
            print(f'[DB] No Azure DB configured. Using local SQLite: {sqlite_path}')

        # Create engine and session factory
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Auto-create tables on first run
        Base.metadata.create_all(bind=self.engine)

    def save_report(self, ticker: str, content: str) -> Optional[int]:
        """
        Persists a completed investment report to the database.

        Args:
            ticker (str): Stock symbol (e.g. 'NVDA').
            content (str): Full Markdown text of the report.

        Returns:
            Optional[int]: The new record ID on success, None on failure.
        """
        session = self.SessionLocal()
        try:
            new_report = FinancialReport(ticker=ticker, content=content)
            session.add(new_report)
            session.commit()
            print(f'[DB] Saved {ticker} report (ID: {new_report.id})')
            return new_report.id
        except Exception as e:
            print(f'[DB] Error saving report: {e}')
            session.rollback()
            return None
        finally:
            # Always close the session to release the connection
            session.close()

    def fetch_reports(self, ticker: str = None) -> list:
        """
        Retrieves saved reports, optionally filtered by ticker.

        Args:
            ticker (str, optional): Filter by symbol. None returns all.

        Returns:
            list[FinancialReport]: List of ORM report objects.
        """
        session = self.SessionLocal()
        try:
            q = session.query(FinancialReport)
            if ticker:
                q = q.filter(FinancialReport.ticker == ticker.upper())
            return q.order_by(FinancialReport.created_at.desc()).all()
        except Exception as e:
            print(f'[DB] Error fetching reports: {e}')
            return []
        finally:
            session.close()