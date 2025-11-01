import sqlite3
import os

# Current folder
DB_PATH = os.path.join(os.getcwd(), "wardrobe.db")  # <-- store DB in py/

# Make sure folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Clothes table
c.execute('''
CREATE TABLE IF NOT EXISTS clothes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    subtype TEXT,
    color TEXT,
    season TEXT,
    occasion TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
# Recommendations table
c.execute('''
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    top TEXT NOT NULL,
    bottom TEXT NOT NULL,
    shoe TEXT NOT NULL,
    season TEXT,
    occasion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')


conn.commit()
conn.close()

print("✅ Database and tables created successfully!")
