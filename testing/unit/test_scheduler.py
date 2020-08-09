import datetime
import unittest

import pytest
import schedule

from utils import scheduler


class TestScheduler(unittest.TestCase):
    def test__check_valid_datetime(self):
        """Tests that a valid at_time is deemed valid"""
        self.assertIsInstance(scheduler._validate_datetime("11:11:11"), datetime.datetime)
        self.assertIsInstance(scheduler._validate_datetime("1:11:11"), datetime.datetime)
        self.assertIsInstance(scheduler._validate_datetime("13:01:00"), datetime.datetime)
        self.assertEqual(scheduler._validate_datetime("0"), "0")

    def test__check_invalid_datetime(self):
        """Tests that an invalid at_time throws an exception"""
        with pytest.raises(BaseException):
            scheduler._validate_datetime("111:11")
        with pytest.raises(BaseException):
            scheduler._validate_datetime("")
        with pytest.raises(BaseException):
            scheduler._validate_datetime("11:11")
        with pytest.raises(BaseException):
            scheduler._validate_datetime("1:11PM")

    def test__check_valid_weekday(self):
        """Tests that a valid weekday is deemed valid"""
        self.assertIsInstance(scheduler._get_weekday("monday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("tuesday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("wednesday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("thursday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("friday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("saturday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("sunday"), schedule.Job)
        self.assertIsInstance(scheduler._get_weekday("MoNdAy"), schedule.Job)

    def test__check_invalid_weekday(self):
        """Tests that an invalid weekday returns None"""
        self.assertIsNone(scheduler._get_weekday("not_a_weekday"))
        self.assertIsNone(scheduler._get_weekday(""))
        self.assertIsNone(scheduler._get_weekday("monda"))
        self.assertIsNone(scheduler._get_weekday("mondayy"))


if __name__ == '__main__':
    unittest.main()
