import sqlite3

with sqlite3.connect("logins.db") as conn:
    conn.execute("CREATE TABLE logins (email TEXT, password TEXT)")
