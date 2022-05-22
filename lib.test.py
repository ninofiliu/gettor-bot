import sqlite3
from typing import List, Tuple, TypedDict
import unittest

from lib import help_text, respond

nb_bridges_per_pool = 3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("CREATE TABLE bridges (value TEXT, pool INT)")
cur.execute("CREATE TABLE users (username TEXT, bridge TEXT, trust FLOAT)")


def fill_db(bridges: List[Tuple], users: List[Tuple]) -> None:
    cur = con.cursor()
    cur.execute("DELETE FROM bridges")
    cur.executemany("INSERT INTO bridges (value, pool) VALUES (?, ?)", bridges)
    cur.execute("DELETE FROM users")
    cur.executemany(
        "INSERT INTO users (username, bridge, trust) VALUES (?, ?, ?)", users
    )


class TestRespond(unittest.TestCase):
    def test_help(self):
        fill_db([], [])

        response = respond(con, "help", "")

        self.assertEqual(response, help_text)

    # User does not exist: should send one bridge at random
    def test_get_bridge_0(self):
        fill_db([("b0", 0), ("b1", 0), ("b2", 0)], [("not-bobby", "b0", 0)])

        response = respond(con, "get_bridge", "bobby")
        self.assertTrue(response in ["b0", "b1", "b2"])

    # User already exists: should send the same bridge when asked several times
    def test_get_bridge_1(self):
        fill_db([("b0", 0), ("b1", 0), ("b2", 0)], [("not-bobby", "b0", 0)])

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
