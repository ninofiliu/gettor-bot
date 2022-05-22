import sqlite3
from typing import List, Tuple
import unittest

from lib import help_text, respond

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("CREATE TABLE bridges (bridge text)")
cur.execute("CREATE TABLE users (username text, bridge text, language text)")


def fill_db(bridges: List[Tuple[str]], users: List[Tuple[str, str]]) -> None:
    cur = con.cursor()
    cur.execute("DELETE FROM bridges")
    cur.executemany("INSERT INTO bridges VALUES (?)", bridges)
    cur.execute("DELETE FROM users")
    cur.executemany("INSERT INTO users VALUES (?, ?)", users)


class TestRespond(unittest.TestCase):
    def test_help(self):
        fill_db([], [])

        response = respond(con, "help", "")

        self.assertEqual(response, help_text)

    # User does not exist: should send one bridge at random
    def test_get_bridge_0(self):
        bridges = ["bridge 1", "bridge 2", "bridge 3"]
        fill_db([(bridge,) for bridge in bridges], [("not-bobby", bridges[2])])

        response = respond(con, "get_bridge", "bobby")
        self.assertTrue(response in bridges)

    # User already exists: should send the same bridge when asked several times
    def test_get_bridge_1(self):
        bridges = ["bridge 1", "bridge 2", "bridge 3"]
        fill_db([(bridge,) for bridge in bridges], [("not-bobby", bridges[2])])

        first_response = respond(con, "get_bridges", "bobby")
        for i in range(10):
            subsequent_response = respond(con, "get_bridges", "bobby")
            self.assertEqual(first_response, subsequent_response)

    # No bridges available: should fail gracefully
    def test_get_bridge_2(self):
        fill_db([], [])

        response = respond(con, "get_bridge", "bobby")
        self.assertEqual(response, "No bridges available")

    def test_default(self):
        fill_db([], [])

        response = respond(
            con,
            "not_a_known_command",
            "",
        )
        self.assertEqual(response, help_text)


if __name__ == "__main__":
    unittest.main()
