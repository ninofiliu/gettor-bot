from typing import Any, List, Union
import unittest

from lib import help_text, respond


def create_fake_db(users: List[Any]):
    def get_bridge(username: str) -> Union[None, str]:
        matches = [b for (u, b) in users if username == u]
        return None if len(matches) == 0 else matches[0]

    def set_bridge(username: str, bridge: str) -> None:
        for i in range(len(users)):
            if users[i][0] == username:
                users[i][1] = bridge
                return

    return get_bridge, set_bridge


class TestRespond(unittest.TestCase):
    def test_help(self):
        get_bridge, set_bridge = create_fake_db([])

        response = respond("help", "", [], get_bridge, set_bridge)

        self.assertEqual(response, help_text)

    # User does not exist: should send one bridge at random
    def test_get_bridge_0(self):
        bridges = ["bridge 1", "bridge 2"]
        get_bridge, set_bridge = create_fake_db([("not-bobby", bridges[0])])

        response = respond("get_bridge", "bobby", bridges, get_bridge, set_bridge)
        self.assertTrue(response in bridges)

    # User already exists: should send the same bridge when asked several times
    def test_get_bridge_1(self):
        bridges = ["bridge 1", "bridge 2"]
        get_bridge, set_bridge = create_fake_db([("not-bobby", bridges[0])])

        first_response = respond(
            "get_bridges", "bobby", bridges, get_bridge, set_bridge
        )
        for i in range(10):
            subsequent_response = respond(
                "get_bridges", "bobby", bridges, get_bridge, set_bridge
            )
            self.assertEqual(first_response, subsequent_response)

    # No bridges available: should fail gracefully
    def test_get_bridge_2(self):
        get_bridge, set_bridge = create_fake_db([])
        response = respond("get_bridge", "bobby", [], get_bridge, set_bridge)
        self.assertEqual(response, "No bridges available")

    def test_default(self):
        response = respond(
            "something that is not a known command", "", [], lambda: None, lambda: None
        )
        self.assertEqual(response, help_text)


if __name__ == "__main__":
    unittest.main()
