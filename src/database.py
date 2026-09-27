import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/netshield.db")


def get_connection():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyst_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flow_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            comment TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_review(flow_id, status, comment):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analyst_reviews
        (flow_id, status, comment, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            int(flow_id),
            status,
            comment,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_reviews(flow_id=None):
    import pandas as pd

    conn = get_connection()

    if flow_id is None:
        query = """
            SELECT
                id,
                flow_id,
                status,
                comment,
                created_at
            FROM analyst_reviews
            ORDER BY created_at DESC
        """

        df = pd.read_sql_query(query, conn)

    else:
        query = """
            SELECT
                id,
                flow_id,
                status,
                comment,
                created_at
            FROM analyst_reviews
            WHERE flow_id = ?
            ORDER BY created_at DESC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(int(flow_id),)
        )

    conn.close()

    return df