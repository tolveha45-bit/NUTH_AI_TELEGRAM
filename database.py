import sqlite3
import time

DB_NAME = "nuth_ai.db"


def connect():
    return sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )


def init_db():

    db = connect()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            timestamp INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            blocked INTEGER DEFAULT 0,
            muted INTEGER DEFAULT 0
        )
    """)

    db.commit()
    db.close()


def save_message(user_id, role, message):

    db = connect()

    db.execute(
        """
        INSERT INTO messages
        (user_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            role,
            message,
            int(time.time())
        )
    )

    db.commit()
    db.close()


def get_history(user_id, limit=20):

    db = connect()

    rows = db.execute(
        """
        SELECT role, message
        FROM messages
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    db.close()

    rows.reverse()

    return rows


def set_setting(key, value):

    db = connect()

    db.execute(
        """
        INSERT OR REPLACE INTO settings
        (key, value)
        VALUES (?, ?)
        """,
        (key, str(value))
    )

    db.commit()
    db.close()


def get_setting(key, default=None):

    db = connect()

    row = db.execute(
        """
        SELECT value
        FROM settings
        WHERE key = ?
        """,
        (key,)
    ).fetchone()

    db.close()

    if row:
        return row[0]

    return default


def add_user(user_id, username, first_name):

    db = connect()

    db.execute(
        """
        INSERT OR REPLACE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            username or "",
            first_name or ""
        )
    )

    db.commit()
    db.close()


def is_blocked(user_id):

    db = connect()

    row = db.execute(
        """
        SELECT blocked
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    db.close()

    return bool(row and row[0])


def is_muted(user_id):

    db = connect()

    row = db.execute(
        """
        SELECT muted
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()

    db.close()

    return bool(row and row[0])


def set_blocked(user_id, value):

    db = connect()

    db.execute(
        """
        UPDATE users
        SET blocked = ?
        WHERE user_id = ?
        """,
        (int(value), user_id)
    )

    db.commit()
    db.close()


def set_muted(user_id, value):

    db = connect()

    db.execute(
        """
        UPDATE users
        SET muted = ?
        WHERE user_id = ?
        """,
        (int(value), user_id)
    )

    db.commit()
    db.close()
