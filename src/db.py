import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "labflow.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT, submitted_by TEXT, workflow TEXT,
            issue_text TEXT, category TEXT, severity TEXT,
            confidence INTEGER, summary TEXT)''')
        conn.commit()

def save_issue(submitted_by, workflow, issue_text, result):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO issues VALUES (NULL,?,?,?,?,?,?,?,?)",
            (datetime.now().isoformat(timespec="seconds"), submitted_by, workflow,
             issue_text, result["category"], result["severity"],
             result["confidence"], result["summary"])
        )
        conn.commit()

def load_issues():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT created_at, submitted_by, workflow, category, severity, summary "
            "FROM issues ORDER BY id DESC", conn)
