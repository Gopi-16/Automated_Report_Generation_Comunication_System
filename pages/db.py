import sqlite3
import bcrypt

def verify_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_hashed_pw = result[0]  # stored as bytes
        if isinstance(stored_hashed_pw, str):  # if stored as str, convert to bytes
            stored_hashed_pw = stored_hashed_pw.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw)
    
    return False
def email_exists(email):
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT 1 from users WHERE email=?",(email,))
    result=c.fetchone()
    conn.close()
    return result is not None

# Always create new connection in the current thread
def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, email, password):
    conn = get_connection()
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM users")
    data = c.fetchall()
    conn.close()
    return data

def update_user_name(email, new_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET name = ? WHERE email = ?", (new_name, email))
    conn.commit()
    conn.close()

def delete_user_by_email(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()

def delete_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
