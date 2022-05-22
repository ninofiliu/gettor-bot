"""
Library part of gettor-bot

It should *not* depend on "services": semaphore, libsignal etc
Instead, use this lib inside files like main.py that use services
This way, this lib
- is pure-python, pure-logic
- works everywhere
- can be easily reused to create bots for other platforms than Signal
- and can be properly unit tested

(* ^ ω ^)
"""

import random
import sqlite3
from typing import List

help_text = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
- get_bridge: sends one bridge info
"""


def respond(
    con: sqlite3.Connection,
    text: str,
    username: str,
) -> str:
    def get_all(table: str) -> List[sqlite3.Row]:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()

    def get_one(table: str, key: str, value):
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE ? = ?", (key, value))
        return cur.fetchone()

    def set_one(
        table: str,
        filter_key,
        filter_value,
        set_key,
        set_value,
    ):
        cur = con.cursor()
        cur.execute(
            f"UPDATE {table} SET {set_key} = ? WHERE {filter_key} = ?",
            (set_value, filter_value),
        )
        con.commit()

    if text == "help":
        return help_text

    if text == "get_bridge":
        bridges = get_all("bridges")
        if len(bridges) == 0:
            return "No bridges available"
        maybe_user = get_one("users", "username", username)
        if maybe_user is None:
            new_bridge = random.choice(bridges)
            set_one("users", "username", username, "bridge", new_bridge["value"])
            return new_bridge["value"]
        else:
            return maybe_user["value"]

    else:
        return help_text
