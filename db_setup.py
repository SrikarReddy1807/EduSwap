import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll TEXT UNIQUE,
    department TEXT,
    password TEXT,
    year TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS skills (
    user_id INTEGER PRIMARY KEY,
    teach_skills TEXT,
    learn_skills TEXT
)
""")

conn.commit()
conn.close()
print("Database created successfully")
