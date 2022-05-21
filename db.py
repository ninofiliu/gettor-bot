import sqlite3
from typing import List, Tuple, TypedDict, Union
from consts import db_file_name

con = sqlite3.connect(db_file_name)

cur = con.cursor()
bridges: List[str] = [bridge for (bridge,) in cur.execute("SELECT * FROM bridges")]


def get_bridge(username: str) -> Union[None, str]:
    matches = list(
        cur.execute(
            "SELECT bridge FROM users WHERE username=:username", {"username": username}
        )
    )
    if len(matches) == 0:
        return None
    return matches[0][0]


def set_bridge(username: str, bridge: str) -> None:
    cur.execute(
        "UPDATE users SET bridge=:bridge WHERE username=:username",
        {"username": username, "bridge": bridge},
    )
