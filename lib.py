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
import re
import sqlite3
from typing import List

from params import max_recs_per_day
from translations import translations


def respond(
    con: sqlite3.Connection,
    text: str,
    username: str,
) -> str:
    def read(query: str, variables=None):
        cur = con.cursor()
        cur.execute(query, variables)
        return cur.fetchall()

    def write(query: str, variables=None):
        cur = con.cursor()
        cur.execute(query, variables)
        con.commit()

    def get_all(table: str) -> List[sqlite3.Row]:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")
        return cur.fetchall()

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

    # if text == "list_languages":
    #     return "en, ru"

    # if text == "choose_language":

    #     lang_match = re.match(r"^choose_language (.*)", text)
    #     if lang_match is not None:
    #         lang = lang_match.group(0)
    #         username, lang

    if text == "help":
        return translations["en"]["help_text"]

    if text == "get_bridge":
        bridges = get_all("bridges")
        if len(bridges) == 0:
            return translations["en"]["no_bridges"]
        users = read("SELECT * FROM users WHERE username = ?", (username,))
        if (len(users)) == 0:
            return "Failed: you are unknown"
        user = users[0]
        if user["trust"] < 0.5:
            return "Failed: you are not trusted enough"
        if user["bridge"] is None:
            new_bridge = random.choice(bridges)
            set_one("users", "username", username, "bridge", new_bridge["value"])
            return new_bridge["value"]
        return user["bridge"]

    recommend_match = re.match("recommend (.+)", text)
    if recommend_match is not None:
        recommenders = read("SELECT * FROM users WHERE username = ?", (username,))
        if len(recommenders) == 0:
            return f"Failed: you are unknown"
        recommender = recommenders[0]

        if recommender["trust"] == 0:
            return f"Failed: you are not trusted yet"

        already_recommended_recently = read(
            "SELECT * FROM recommendations WHERE src = ? AND ts > DATETIME('now', '-1 DAYS')",
            (username,),
        )
        if len(already_recommended_recently) > max_recs_per_day:
            return f"Can't recomment more than {max_recs_per_day} users per day"

        recommendee_username = recommend_match.group(1)
        already_recommended_same = read(
            "SELECT * FROM recommendations WHERE src = ? AND dst = ?",
            (username, recommendee_username),
        )
        if len(already_recommended_same) > 0:
            return f"You already recommended {recommendee_username}"

        recommendees = read(
            "SELECT * FROM users WHERE username = ?", (recommendee_username,)
        )
        if len(recommendees) == 0:
            new_trust = recommender["trust"] / 2
            write(
                "INSERT INTO users (username, trust) VALUES (?, ?)",
                (recommendee_username, new_trust),
            )
            write(
                "INSERT INTO recommendations (src, dst) VALUES (?, ?)",
                (username, recommendee_username),
            )
            return f"Successfully recommended {recommendee_username}"

        recommendee = recommendees[0]
        if recommendee["trust"] > recommender["trust"]:
            return f"{recommendee_username} is already more trusted than you. You can recommend someone else."

        updated_trust = (recommendee["trust"] + recommender["trust"]) / 2
        write(
            "UPDATE users SET trust = ? WHERE username = ?",
            (updated_trust, recommendee_username),
        )
        write(
            "INSERT INTO recommendations (src, dst) VALUES (?, ?)",
            (username, recommendee_username),
        )
        return f"Successfully improved trust of {recommendee_username}"

    else:
        return translations["en"]["help_text"]
