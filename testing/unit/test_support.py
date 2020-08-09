import filecmp
import shutil
import unittest

from sneaselcommands import support
from utils import file_wrapper
import asyncio


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

    def test__update_leaderboards(self):
        """Tests that nicknames in leaderboards are successfully renamed"""
        original_file = "testBoard.txt"
        copied_file = "testBoard2.txt"
        copied_file2 = "testBoard3.txt"

        # create test leaderboard file
        loop = asyncio.new_event_loop()
        loop.run_until_complete(file_wrapper.create_file(original_file))

        # copy original file to verify later
        shutil.copy(original_file, copied_file)

        # add test entry to totalxp leaderboard file
        file_wrapper.append_to_file("McTestOriginal", original_file)
        shutil.copy(original_file, copied_file2)

        # test changing nickname
        support._update_leaderboards("McTestOriginal", "McTestNew", original_file)
        self.assertTrue(file_wrapper.found_in_file("McTestNew", original_file))
        self.assertFalse(file_wrapper.found_in_file("McTestOriginal", original_file))

        # test changing nickname back
        support._update_leaderboards("McTestNew", "McTestOriginal", original_file)
        self.assertFalse(file_wrapper.found_in_file("McTestNew", original_file))
        self.assertTrue(file_wrapper.found_in_file("McTestOriginal", original_file))

        # compare files must be completely equal after 2 calls
        self.assertTrue(filecmp.cmp(original_file, copied_file2))

        # remove test name from file again
        file_wrapper.remove_line_from_file("McTestOriginal", original_file)
        self.assertTrue(filecmp.cmp(original_file, copied_file))

        file_wrapper.delete_file(original_file)
        file_wrapper.delete_file(copied_file)
        file_wrapper.delete_file(copied_file2)


if __name__ == '__main__':
    unittest.main()
