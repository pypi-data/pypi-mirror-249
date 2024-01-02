# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import unittest

from australians_calendar import Holiday, get_holiday_detail, is_holiday, is_workday


class BasicTests(unittest.TestCase):
    def test_opposite(self):
        date = datetime.date.today()
        self.assertEqual(not is_workday(date), is_holiday(date))

    def test_holidays(self):
        dates = [
            datetime.date(year=2023, month=1, day=26),
            datetime.date(year=2023, month=4, day=8),
            datetime.date(year=2024, month=4, day=1),
            datetime.date(year=2024, month=6, day=10),
        ]
        for date in dates:
            self.assertFalse(is_workday(date))
            self.assertTrue(is_holiday(date))

    def test_workdays(self):
        dates = [
            datetime.date(year=2023, month=1, day=25),
            datetime.date(year=2023, month=4, day=26),
            datetime.date(year=2024, month=10, day=3),
            datetime.date(year=2024, month=12, day=24),
        ]
        for date in dates:
            self.assertFalse(is_holiday(date))
            self.assertTrue(is_workday(date))

    def test_detail(self):
        cases = [
            ((2024, 6, 10), (True, Holiday.kings_birthday.value)),
            ((2024, 12, 25), (True, Holiday.christmas_day.value)),
        ]
        for date, expected_result in cases:
            self.assertEqual(expected_result, get_holiday_detail(datetime.date(*date)))

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            is_holiday(datetime.date(year=2001, month=1, day=1))
