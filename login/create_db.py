import sqlite3

with sqlite3.connect("database.db") as conn:
    conn.execute("CREATE TABLE login")