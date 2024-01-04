import unittest

from cmeel_example import cmeel_add, cmeel_sub


class TestAdder(unittest.TestCase):
    def test_adder_integers(self):
        self.assertEqual(cmeel_add(4, 3), 7)
        self.assertEqual(cmeel_sub(4, 3), 1)


if __name__ == "__main__":
    unittest.main()
