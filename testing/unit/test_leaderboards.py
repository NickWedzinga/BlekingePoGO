import unittest
from sneaselcommands import leaderboards
import pytest


class TestLeaderboards(unittest.TestCase):
    def test__validate_score_valid(self):
        """Tests validate score for a valid score"""
        leaderboards._validate_score("1337")

    def test__validate_score_valid_with_comma(self):
        """Tests validate score for a valid score"""
        leaderboards._validate_score("1,1")

    def test__validate_score_not_a_float(self):
        """Tests validate score for a string instead of float"""
        with pytest.raises(AssertionError):
            leaderboards._validate_score("not_a_score")


if __name__ == '__main__':
    unittest.main()