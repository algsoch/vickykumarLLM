import sqlite3

def get_db_connection():
    """Connects to SQLite database."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
