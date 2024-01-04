# system modules
import logging
import unittest
import datetime
from datetime import datetime as dt, timedelta
from unittest import TestCase

# internal modules
from annextimelog.event import Event


class EventTest(TestCase):
    @staticmethod
    def today(**kwargs):
        return dt.now().replace(
            **{**dict(hour=0, minute=0, second=0, microsecond=0), **kwargs}
        )

    @staticmethod
    def days(n):
        return datetime.timedelta(days=n)

    def test_parse_date(self):
        today, days = self.today, self.days
        for string, shouldbe in {
            "0": today(hour=0),
            "00": today(hour=0),
            "000": today(hour=0),
            "0000": today(hour=0),
            "100": today(hour=1),
            "8": today(hour=8),
            "y1500": today(hour=15) - days(1),
            "t100": today(hour=1) + days(1),
            "yt100": today(hour=1),
            "yytt14:00": today(hour=14),
            "ytt00": today(hour=0) + days(1),
            (s := "2023-01-01T13:00"): dt.fromisoformat(s),
            "2023-01-01 1300": dt(2023, 1, 1, 13),
        }.items():
            with self.subTest(string=string, shouldbe=shouldbe):
                self.assertEqual(
                    (d := Event.parse_date(string)),
                    shouldbe,
                    msg=f"\nEvent.parse_date({string!r}) should be {shouldbe} but is instead {d}",
                )

    def test_parse_date_now(self):
        self.assertLess(Event.parse_date("now") - dt.now(), timedelta(seconds=10))

    def test_to_from_cli_idempotent(self):
        e1 = Event.from_cli(["person=me", "work"])
        e2 = Event.from_cli(e1.to_cli())
        self.assertEqual(e1, e2)

    def test_equality(self):
        def test(method, e1, e2):
            method(e1, e2)
            method(e2, e1)

        test(self.assertEqual, Event(), Event())
        test(self.assertNotEqual, Event(), Event(fields=dict(bla=set(["blubb"]))))
        test(
            self.assertEqual,
            Event(fields=dict(bla=set(["blubb"]))),
            Event.from_cli(["bla=blubb"]),
        )


if __name__ == "__main__":
    unittest.main()
