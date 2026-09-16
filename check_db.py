import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

print("USERS:")
cur.execute("SELECT * FROM users")
print(cur.fetchall())

print("\nSKILLS:")
cur.execute("SELECT * FROM skills")
print(cur.fetchall())

print("\nSESSIONS:")
cur.execute("SELECT * FROM sessions")
print(cur.fetchall())

conn.close()