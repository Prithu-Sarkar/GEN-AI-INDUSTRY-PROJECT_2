
from __future__ import annotations
import sqlite3, sys
from pathlib import Path
sys.path.insert(0, "/content/customer_support_agent/src")
from core.settings import ensure_directories, get_settings

def connect():
    s = get_settings(); ensure_directories(s)
    conn = sqlite3.connect(str(s.db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def row_to_dict(row): return dict(row) if row is not None else None

def init_db():
    """Create all tables + trigger. Safe to call multiple times."""
    with connect() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL,
                name TEXT, company TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER REFERENCES customers(id),
                subject TEXT NOT NULL, description TEXT NOT NULL,
                status TEXT DEFAULT 'open', priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER REFERENCES tickets(id),
                content TEXT NOT NULL, context_used TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TRIGGER IF NOT EXISTS tickets_updated_at
            AFTER UPDATE ON tickets FOR EACH ROW BEGIN
                UPDATE tickets SET updated_at=CURRENT_TIMESTAMP WHERE id=OLD.id;
            END;
        """)
