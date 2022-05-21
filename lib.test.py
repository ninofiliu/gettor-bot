import unittest
from lib import help_text, respond


class TestRespond(unittest.TestCase):
    def test_help(self):
        response = respond("help", "", [], {})
        self.assertEqual(response, help_text)

    # User does not exist: should send one bridge at random
    def test_get_bridge_0(self):
        bridges = ["bridge 1", "bridge 2"]
        response = respond("get_bridge", "bobby", bridges, {"not-bobby": bridges[0]})
        self.assertTrue(response in bridges)

    # User already exists: should send the same bridge when asked several times
    def test_get_bridge_1(self):
        bridges = ["bridge 1", "bridge 2"]
        first_response = respond(
            "get_bridges", "bobby", bridges, {"not-bobby": bridges[0]}
        )
        for i in range(10):
            subsequent_response = respond(
                "get_bridges", "bobby", bridges, {"not-bobby": bridges[0]}
            )
            self.assertEqual(first_response, subsequent_response)

    def test_default(self):
        response = respond("something that is not a known command", "", [], {})
        self.assertEqual(response, help_text)


if __name__ == "__main__":
    unittest.main()
