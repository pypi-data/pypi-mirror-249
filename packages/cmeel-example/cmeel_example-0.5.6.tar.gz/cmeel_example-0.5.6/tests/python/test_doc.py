import doctest
import unittest

import cmeel_example.mult


class TestDoc(unittest.TestCase):
    def test_doc(self):
        failure_count, test_count = doctest.testmod(cmeel_example.mult)
        self.assertEqual(failure_count, 0)
        self.assertGreater(test_count, 0)


if __name__ == "__main__":
    unittest.main()
