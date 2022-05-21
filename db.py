import sqlite3
from typing import List, Tuple, TypedDict, Union
from consts import db_file_name

con = sqlite3.connect(db_file_name)

cur = con.cursor()
bridges: List[str] = [bridge for (bridge,) in cur.execute("SELECT * FROM bridges")]


class User:
    username: str
    bridge: str

    def __init__(self, db_user: Tuple[str, str]) -> None:
        self.username = db_user[0]
        self.bridge = db_user[1]
