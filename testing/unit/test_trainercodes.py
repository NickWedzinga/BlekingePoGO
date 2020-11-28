import unittest

from sneaselcommands import trainercode


class TestTrainerCodes(unittest.TestCase):
    def test__check_invalid_nickname__valid_name(self):
        """Tests that a valid nickname is deemed valid"""
        self.assertEqual(
            first=trainercode.format_trainer_code("111122223333"),
            second="1111 2222 3333"
        )


if __name__ == '__main__':
    unittest.main()
