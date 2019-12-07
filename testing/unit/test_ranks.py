import unittest
from discord.ext import commands  # testing discord lib install for unittests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
