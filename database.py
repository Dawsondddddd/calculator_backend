import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "calculator.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result     TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_history(expression, result_text):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO calculation_history (expression, result, created_at) "
            "VALUES (?, ?, ?)",
            (expression, result_text, created_at),
        )
        return cursor.lastrowid, created_at


def list_history():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, expression, result, created_at "
            "FROM calculation_history ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def delete_history(record_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM calculation_history WHERE id = ?", (record_id,)
        )
        return cursor.rowcount > 0


def clear_history():
    with get_connection() as connection:
        connection.execute("DELETE FROM calculation_history")
