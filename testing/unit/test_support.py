import unittest

from sneaselcommands import support


class TestSupport(unittest.TestCase):
    def test__check_invalid_nickname__valid_name(self):
        """Tests that a valid nickname is deemed valid"""
        self.assertFalse(support._check_invalid_nickname("testName"))

    def test__check_invalid_nickname__name_too_long(self):
        """Tests that a nickname that is too long is deemed invalid"""
        self.assertEqual(
            first=support._check_invalid_nickname("testnameeeeeeeee"),
            second="Your Discord nickname is too long, please change it to match your nickname from Pokémon GO.")

    def test__check_invalid_nickname__illegal_character_hyphen(self):
        """Tests that a nickname that has illegal character '-' is deemed invalid"""
        self.assertEqual(
            first=support._check_invalid_nickname("test-name"),
            second="Your Discord nickname contains illegal characters, please change it to match your nickname from "
                   "Pokémon GO."
        )

    def test__check_invalid_nickname__illegal_character_swedish_a(self):
        """Tests that a nickname that has illegal character 'ä' is deemed invalid"""
        self.assertEqual(
            first=support._check_invalid_nickname("tästname"),
            second="Your Discord nickname contains illegal characters, please change it to match your nickname from "
                   "Pokémon GO."
        )

    def test__check_invalid_nickname__illegal_character_dot(self):
        """Tests that a nickname that has illegal character '.' is deemed invalid"""
        self.assertEqual(
            first=support._check_invalid_nickname("test.name"),
            second="Your Discord nickname contains illegal characters, please change it to match your nickname from "
                   "Pokémon GO."
        )


if __name__ == '__main__':
    unittest.main()
