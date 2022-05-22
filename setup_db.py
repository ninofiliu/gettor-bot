"""
Remove any existing database and sets up the tables for new one
"""

import os
from sqlite3 import connect

nb_bridges_per_pool = 3


try:
    os.remove("db.db")
except:
    pass
con = connect("db.db")
cur = con.cursor()
cur.execute("CREATE TABLE bridges (value TEXT, pool INT)")
file = open("./bridges.txt")
bridges = [line[:-1] for line in file]
for i in range(len(bridges)):
    cur.execute(
        "INSERT INTO bridges (value, pool) VALUES (?, ?)",
        (bridges[i], i // nb_bridges_per_pool),
    )
cur.execute("CREATE TABLE users (username TEXT, bridge TEXT, trust FLOAT, lang TEXT)")
cur.execute(
    "CREATE TABLE recommendations (src TEXT, dst TEXT, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
)
con.commit()
