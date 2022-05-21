"""
Remove any existing database and sets up the tables for new one
"""

import os
from sqlite3 import connect

try:
    os.remove("db.db")
except:
    pass
con = connect("db.db")
cur = con.cursor()
cur.execute("CREATE TABLE bridges (bridge text)")
file = open("./bridges.txt")
for line in file:
    cur.execute("INSERT INTO bridges VALUES (?)", (line[:-1],))
cur.execute("CREATE TABLE users (username text, bridge text)")
con.commit()
