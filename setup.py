import os
import sqlite3
from consts import db_file_name

os.remove(db_file_name)

con = sqlite3.connect(db_file_name)
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
