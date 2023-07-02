import unittest

from sneaselcommands.leaderboards.support import Support


class TestSupport(unittest.TestCase):
    def test__handle_rename_input_syntax_errors__name_too_long(self):
        """Tests that nickname longer than 15 characters returns true for too long name"""
        support = Support()
        name_too_long, _, _ = \
            support._Support__handle_rename_input_syntax_errors("a" * 16, 'some-user-id', 'some-old-name')
        self.assertTrue(name_too_long)

    def test__handle_rename_input_syntax_errors__name_not_too_long(self):
        """Tests that nickname equal to 15 characters returns false for too long name"""
        support = Support()
        name_too_long, _, _ = \
            support._Support__handle_rename_input_syntax_errors("a" * 15, 'some-user-id', 'some-old-name')
        self.assertFalse(name_too_long)

    def test__handle_rename_input_syntax_errors__user_id_non_digit(self):
        """Tests that a non-digit user-id returns true for id not a number check"""
        support = Support()
        _, id_non_number, _ = \
            support._Support__handle_rename_input_syntax_errors("a" * 15, 'non-digit-user-id', 'some-old-name')
        self.assertTrue(id_non_number)

    def test__handle_rename_input_syntax_errors__user_id_digit(self):
        """Tests that a digit-only user-id returns false for id not a number check"""
        support = Support()
        _, id_non_number, _ = \
            support._Support__handle_rename_input_syntax_errors("a" * 16, '12354', 'some-old-name')
        self.assertFalse(id_non_number)

    def test__handle_rename_input_syntax_errors__name_doesnt_match_old_name(self):
        """Tests that mismatching new/old names returns true for name not updated"""
        support = Support()
        _, _, name_not_updated = \
            support._Support__handle_rename_input_syntax_errors("new-name", 'some-user-id', 'old-name')
        self.assertTrue(name_not_updated)

    def test__handle_rename_input_syntax_errors__name_matches_old_name(self):
        """Tests that matching new/old names returns false for name not updated"""
        support = Support()
        _, _, name_not_updated = \
            support._Support__handle_rename_input_syntax_errors("new-name", 'some-user-id', 'new-name')
        self.assertFalse(name_not_updated)


if __name__ == '__main__':
    unittest.main()
