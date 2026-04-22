# database.py
import sqlite3
import os

def create_connection():
    # 1. Pehle check karo ki 'data' folder hai ya nahi, agar nahi toh bana do
    os.makedirs('data', exist_ok=True)
    
    # 2. Ab safely database file connect/create karo
    conn = sqlite3.connect('data/health_database_v2.db')
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()
    
    # Users Table
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
        c.execute('INSERT INTO users (email, phone, dob, username, password) VALUES (?, ?, ?, ?, ?)', 
                  (email, phone, dob, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False 
    finally:
        conn.close()

def login_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    conn.close()
    return data
