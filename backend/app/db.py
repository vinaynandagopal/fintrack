import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "fintrack_user"),
            password=os.getenv("DB_PASSWORD", "Fintrack@12345"),
            database=os.getenv("DB_NAME", "fintrack_db"),
            port=int(os.getenv("DB_PORT", "3306")),
        )
    except Error as exc:
        raise RuntimeError(f"Database connection failed: {exc}") from exc

def fetch_one(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def fetch_all(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id