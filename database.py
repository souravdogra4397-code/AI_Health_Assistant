# database.py
# Author: Bikram Singh
import sqlite3

def create_connection():
    # Naya database name taaki purani error wali file se koi lafda na rahe
    conn = sqlite3.connect('data/health_database_v2.db')
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()
    
    # Users Table (Exactly 5 columns: email, phone, dob, username, password)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            phone TEXT,
            dob TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Medical History Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            symptoms TEXT,
            prediction TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email, phone, dob, username, password):
    conn = create_connection()
    c = conn.cursor()
    try:
        # Exactly 5 values ja rahi hain table mein
        c.execute('INSERT INTO users (email, phone, dob, username, password) VALUES (?, ?, ?, ?, ?)', 
                  (email, phone, dob, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Jab username pehle se exist karta ho
    finally:
        conn.close()

def login_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    conn.close()
    return data