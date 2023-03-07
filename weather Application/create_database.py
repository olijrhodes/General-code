import sqlite3

with sqlite3.connect("tables.db") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE areas (name TEXT)")
    cur.execute("CREATE TABLE log (location TEXT, temp REAL, search_time TEXT )")

def fill_table():
    area_list = ["Birmingham", "Leeds", "Bristol", "london", "Manchester", "Exceter"]
    with sqlite3.connect ("tables.db") as conn:
        cur = conn.cursor()
        for area in area_list:
            cur.execute("INSERT INTO areas (name) VALUES (?)", (area,))

fill_table()