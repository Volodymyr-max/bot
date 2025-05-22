import sqlite3
from datetime import datetime, timedelta

DB_FILE = "users.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

def get_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(user_id, nickname, game_id, name, region, age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, nickname, game_id, name, region, age, last_updated, is_banned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, nickname, game_id, name, region, age, datetime.now(), 0))
    conn.commit()
    conn.close()

def update_user(user_id, field, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ?, last_updated = ? WHERE user_id = ?", (value, datetime.now(), user_id))
    conn.commit()
    conn.close()

def update_user_activity(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_active = ? WHERE user_id = ?", (datetime.now(), user_id))
    conn.commit()
    conn.close()

def is_banned(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1

def set_ban_status(user_id, status=True):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_banned = ? WHERE user_id = ?", (1 if status else 0, user_id))
    conn.commit()
    conn.close()

def get_inactive_users(days=7):
    conn = connect_db()
    cursor = conn.cursor()
    threshold = datetime.now() - timedelta(days=days)
    cursor.execute("SELECT * FROM users WHERE last_active IS NULL OR last_active < ?", (threshold,))
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
