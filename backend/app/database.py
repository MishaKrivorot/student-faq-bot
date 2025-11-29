# backend/app/database.py
import sqlite3
from typing import Generator

DB_PATH = "app/faqs.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
