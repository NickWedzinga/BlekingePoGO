import unittest

from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController


class TestLeaderboards(unittest.TestCase):
    def test__validate_score_valid(self):
        """Tests validate score for a valid score"""
        self.assertTrue(LeaderboardController.validate_score("1337"))

    def test__validate_score_valid_with_comma(self):
        """Tests validate score for a valid score"""
        self.assertFalse(LeaderboardController.validate_score("1,1"))

    def test__validate_score_not_a_float(self):
        """Tests validate score for a string instead of float"""
        self.assertFalse(LeaderboardController.validate_score("not_a_score"))


if __name__ == '__main__':
    unittest.main()
