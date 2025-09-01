import sqlite3
import os

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            text TEXT,
            sentiment TEXT,
            FOREIGN KEY(account_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        account_id = c.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return None
    conn.close()
    return account_id


def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def save_history(account_id, text, sentiment):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO history (account_id, text, sentiment) VALUES (?, ?, ?)", (account_id, text, sentiment))
    conn.commit()
    conn.close()


def get_history(account_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT text, sentiment FROM history WHERE account_id=?", (account_id,))
    rows = c.fetchall()
    conn.close()
    return [{"text": r[0], "sentiment": r[1]} for r in rows]


def is_admin(account_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1


def list_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin FROM users")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "username": r[1], "is_admin": bool(r[2])} for r in rows]
