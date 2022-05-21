import unittest
from lib import help_text, respond


class TestRespond(unittest.TestCase):
    def test_help(self):
        self.assertEqual(respond("help"), help_text)

    def test_default(self):
        self.assertEqual(respond("something that is not a known command"), help_text)


if __name__ == "__main__":
    unittest.main()
