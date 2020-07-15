import unittest

from sneaselcommands.ranks import _create_rank_string, _build_rank_message, _extract_score, _every_fifteenth_or_last


class TestRanks(unittest.TestCase):

    def test_create_rank_string_top_10(self):
        """Testing creating a detailed rank string for a top ten submission"""
        self.assertEqual(
            first=_create_rank_string(4, "test_name", "test_leaderboard", "test_score"),
            second=":keycap_four: test_name is ranked #4 in the Test_leaderboard leaderboard with"
                   " a score of test_score."
        )

    def test_create_rank_string_low_rank(self):
        """Testing creating a detailed rank string for a rank 11 submission"""
        self.assertEqual(
            first=_create_rank_string(11, "test_name", "test_leaderboard", "test_score"),
            second=":asterisk: test_name is ranked #11 in the Test_leaderboard leaderboard with"
                   " a score of test_score."
        )

    def test_build_rank_message(self):
        """Testing building message from list"""
        test_list = ["test_1", "test_2"]
        self.assertEqual(
            first=_build_rank_message(test_list, 0, 2),
            second="test_1\ntest_2"
        )

    def test_extract_score(self):
        """Testing extracting score from leaderboard entry"""
        self.assertEqual(
            first=_extract_score("test_name test_score 2019-12-07"),
            second="test_score"
        )

    def test_every_fifteenth_or_last_15(self):
        """Testing leaderboard split counting function"""
        self.assertTrue(_every_fifteenth_or_last(15, 16))

    def test_every_fifteenth_or_last_last(self):
        """Testing leaderboard split counting function"""
        self.assertTrue(_every_fifteenth_or_last(16, 16))

    def test_every_fifteenth_or_last_negative(self):
        """Testing leaderboard split counting function"""
        self.assertFalse(_every_fifteenth_or_last(1, 16))


if __name__ == '__main__':
    unittest.main()
