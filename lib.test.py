import sqlite3
import unittest
from datetime import datetime, timedelta
from select import select
from typing import List, Tuple, TypedDict

from lib import help_text_en, respond
from params import max_recs_per_day

nb_bridges_per_pool = 3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("CREATE TABLE bridges (value TEXT, pool INT)")
cur.execute("CREATE TABLE users (username TEXT, bridge TEXT, trust FLOAT)")
cur.execute(
    "CREATE TABLE recommendations (src TEXT, dst TEXT, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
)


def fill_db(
    bridges: List[Tuple] = [],
    users: List[Tuple] = [],
    recommendations: List[Tuple] = [],
) -> None:
    cur = con.cursor()
    cur.execute("DELETE FROM bridges")
    cur.executemany("INSERT INTO bridges (value, pool) VALUES (?, ?)", bridges)
    cur.execute("DELETE FROM users")
    cur.executemany(
        "INSERT INTO users (username, bridge, trust) VALUES (?, ?, ?)", users
    )
    cur.execute("DELETE FROM recommendations")
    cur.executemany(
        "INSERT INTO recommendations (src, dst, ts) VALUES (?, ?, ?)", recommendations
    )


class TestRespond(unittest.TestCase):
    def assert_db_equals(
        self,
        bridges: List[Tuple] = [],
        users: List[Tuple] = [],
        recommendations: List[Tuple] = [],
    ) -> None:
        cur = con.cursor()
        self.assertEqual(
            [
                (list(row)[0], list(row)[1])
                for row in cur.execute("SELECT * FROM bridges").fetchall()
            ],
            bridges,
        )
        self.assertEqual(
            [
                (list(row)[0], list(row)[1], list(row)[2])
                for row in cur.execute("SELECT * FROM users").fetchall()
            ],
            users,
        )
        self.assertEqual(
            [
                (list(row)[0], list(row)[1])  # do not check time stamp
                for row in cur.execute("SELECT * FROM recommendations").fetchall()
            ],
            recommendations,
        )

    ## help

    def test_help(self):
        fill_db()

        response = respond(con, "help", "bobby")

        self.assertEqual(response, help_text_en)

    ## get_bridge

    # User does not exist: should send one bridge at random
    def test_get_bridge_0(self):
        fill_db(
            bridges=[("b0", 0), ("b1", 0), ("b2", 0)], users=[("not-bobby", "b0", 0)]
        )

        response = respond(con, "get_bridge", "bobby")
        self.assertTrue(response in ["b0", "b1", "b2"])

    # User already exists: should send the same bridge when asked several times
    def test_get_bridge_1(self):
        fill_db(
            bridges=[("b0", 0), ("b1", 0), ("b2", 0)], users=[("not-bobby", "b0", 0)]
        )

        first_response = respond(con, "get_bridges", "bobby")
        for i in range(10):
            subsequent_response = respond(con, "get_bridges", "bobby")
            self.assertEqual(first_response, subsequent_response)

    # No bridges available: should fail gracefully
    def test_get_bridge_2(self):
        fill_db()

        response = respond(con, "get_bridge", "bobby")
        self.assertEqual(response, "No bridges available")

    ## recommend

    # No specified username: should respond with help text
    def test_recommend_0(self):
        fill_db()
        response = respond(con, "recommend", "bobby")
        self.assertEqual(response, help_text_en)

    # Unknown recommender
    def test_recommend_1(self):
        fill_db()
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(response, "Failed: you are unkown")

    # Untrusted recommender
    def test_recommend_2(self):
        fill_db(users=[("bobby", None, 0)])
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(response, "Failed: you are not trusted yet")

    # Too many recommendations
    def test_recommend_3(self):
        fill_db(
            users=[("bobby", None, 0.8)],
            recommendations=[
                ("bobby", f"friend of bobby #{i}", datetime.now())
                for i in range(2 * max_recs_per_day)
            ],
        )
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(response, "Can't recomment more than 5 users per day")

    # Already recommended
    def test_recommend_4(self):
        fill_db(
            users=[("bobby", None, 0.8), ("charlie", None, 0.4)],
            recommendations=[("bobby", "charlie", datetime.now() - timedelta(days=2))],
        )
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(response, "You already recommended charlie")

    # Recomendee does not exist yet
    def test_recommend_5(self):
        fill_db(
            users=[("bobby", None, 0.8)],
        )
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(response, "Successfully recommended charlie")
        self.assert_db_equals(
            users=[("bobby", None, 0.8), ("charlie", None, 0.4)],
            recommendations=[("bobby", "charlie")],
        )

    # Recomendee exists and is more trustworthy
    def test_recommend_6(self):
        users = [("bobby", None, 0.5), ("charlie", None, 0.8)]
        fill_db(
            users=users,
        )
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(
            response,
            "charlie is already more trusted than you. You can recommend someone else.",
        )
        self.assert_db_equals(
            users=users,
            recommendations=[],
        )

    # Recomendee exists and is less trustworthy
    def test_recommend_7(self):
        fill_db(
            users=[("bobby", None, 0.8), ("charlie", None, 0.2)],
        )
        response = respond(con, "recommend charlie", "bobby")
        self.assertEqual(
            response,
            "Successfully improved trust of charlie",
        )
        self.assert_db_equals(
            users=[("bobby", None, 0.8), ("charlie", None, 0.5)],
            recommendations=[("bobby", "charlie")],
        )

    ## default

    def test_default(self):
        fill_db()

        response = respond(
            con,
            "not_a_known_command",
            "bobby",
        )
        self.assertEqual(response, help_text_en)


if __name__ == "__main__":
    unittest.main()
