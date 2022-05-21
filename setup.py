import os
import sqlite3

os.remove("db.db")

con = sqlite3.connect("db.db")
cur = con.cursor()

bridges = []
with open("./bridges.txt") as bridgesFile:
    for line in bridgesFile:
        bridges.append((line[0 : len(line) - 1],))
cur.execute("CREATE TABLE bridges (bridge text)")
cur.executemany("INSERT INTO bridges VALUES (?)", bridges)

cur.execute("CREATE TABLE users (username text, bridge text)")

con.commit()
con.close()
