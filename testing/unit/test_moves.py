import unittest

from sneasel_types import moves


class TestMoves(unittest.TestCase):
    def test__init_default(self):
        """Tests default init"""
        self.assertIsNone(moves.Moves().fast_moves)
        self.assertIsNone(moves.Moves().charge_moves)

    def test__extraction(self):
        """Tests init by providing value for moves lists"""
        test_fast_moves = ["TEST_1FAST_FAST", "TEST_2FAST_FAST"]
        test_charge_moves = ["TEST1_CHARGE", "TEST2_CHARGE"]

        test_moves = moves.Moves(test_fast_moves, test_charge_moves)

        self.assertEqual(test_moves.fast_moves, ["TEST 1FAST\n", "TEST 2FAST\n"])
        self.assertEqual(test_moves.charge_moves, ["TEST1 CHARGE\n", "TEST2 CHARGE\n"])

    def test__toString_override(self):
        """Tests toString override"""
        test_fast_moves = ["TEST_1FAST_FAST", "TEST_2FAST_FAST"]
        test_charge_moves = ["TEST1_CHARGE", "TEST2_CHARGE"]
        test_moves = moves.Moves(test_fast_moves, test_charge_moves)
        
        self.assertEqual(test_moves.__str__(), f"Fast moves: {test_moves.fast_moves}, charge moves: {test_moves.charge_moves}")


if __name__ == '__main__':
    unittest.main()