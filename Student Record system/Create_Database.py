import sqlite3

conn = sqlite3.connect("Students.db")
print("Successfully created database")

try:
    conn.execute("CREATE TABLE students (name TEXT, id TEXT, addr TEXT, city TEXT)")
    print("Table created")
except Exception:
    print("Table already exists")

conn.close()