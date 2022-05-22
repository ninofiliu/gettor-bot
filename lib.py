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

from distutils.command.config import LANG_EXT
import random
import re
import sqlite3
from typing import List

help_text_en = """
I did not undestand your message.

Please text me one of:

- help: sends this current help message
- get_bridge: sends one bridge info
"""

help_text_ru = """
Сообщение не распознано.

Доступные команды:

- help: отправляет текущее сообщение помощи
- get_bridge: отправляет адрес моста
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

    if text == "list_languages":

        return "en, ru"

    # GURL PLEASE HELP ME

    if text == "choose_language":

        lang_match = re.match(r"^choose_language (.*)", text)
        if lang_match is not None:
            lang = lang_match.group(0)
            username, lang

    if text == "help":

        translation = {
            "en": {"help_text": help_text_en},
            "ru": {"help_text": help_text_ru},
        }

        return translation[lang]["help_text"]

    if text == "get_bridge":
        bridges = get_all("bridges")
        if len(bridges) == 0:

            translation = {
                "en": {"no_bridges": "No bridges available"},
                "ru": {"no_bridges": "Нет доступных мостов"},
            }
            return translation[lang]["no_bridges"]

        maybe_user = get_one("users", "username", username)
        if maybe_user is None:
            new_bridge = random.choice(bridges)
            set_one("users", "username", username, "bridge", new_bridge["bridge"])
            return new_bridge["bridge"]
        else:
            return maybe_user["bridge"]

    else:
        return translation[lang]["help_text"]
