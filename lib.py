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
from typing import List, Tuple, Union

help_text = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
- get_bridge: sends one bridge info
"""


def get_bridges(con: sqlite3.Connection) -> List[str]:
    cur = con.cursor()
    cur.execute("SELECT bridge FROM bridges")
    return [bridge for (bridge,) in cur.fetchall()]


def get_bridge(con: sqlite3.Connection, username: str) -> Union[None, str]:
    cur = con.cursor()
    cur.execute("SELECT bridge FROM users WHERE username=?", (username,))
    one = cur.fetchone()
    return None if one is None else one[0]


def set_bridge(con: sqlite3.Connection, username: str, bridge: str) -> None:
    cur = con.cursor()
    cur.execute("UPDATE users SET bridge = ? WHERE username = ?", (bridge, username))
    con.commit()


def respond(
    con: sqlite3.Connection,
    text: str,
    username: str,
) -> str:
    if text == "help":
        return help_text
    if text == "get_bridge":
        bridges = get_bridges(con)
        if len(bridges) == 0:
            return "No bridges available"
        maybe_bridge = get_bridge(con, username)
        if maybe_bridge is None:
            new_bridge = random.choice(bridges)
            set_bridge(con, username, new_bridge)
            return new_bridge
        else:
            return maybe_bridge
    else:
        return help_text
