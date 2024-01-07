# system modules
import logging
import unittest
import shlex
from datetime import datetime as dt, datetime, timedelta as td, timedelta
from unittest import TestCase

# internal modules
from annextimelog.event import Event
from annextimelog.token import *

logger = logging.getLogger(__name__)


def today(**kwargs):
    return dt.now().replace(
        **{**dict(hour=0, minute=0, second=0, microsecond=0), **kwargs}
    )


def days(n):
    return timedelta(days=n)


class TokenTest(TestCase):
    def test_fieldmodifier(self):
        for s, r in {
            "a": AddToField("", "tag", {"a"}),
            "tag+=until": AddToField("", "tag", {"until"}),
            "tag+=a,b,c": AddToField("", "tag", {"a", "b", "c"}),
            "tags+=a,b,c": AddToField("", "tag", {"a", "b", "c"}),
            "tags-=a,b,c": RemoveFromField("", "tag", {"a", "b", "c"}),
            "tags=a,b,c": SetField("", "tag", {"a", "b", "c"}),
            "tags=": UnsetField("", "tag"),
            "field=": UnsetField("", "field"),
            "@home": SetField("", "location", {"home"}),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(Token.from_str(s), r)

    def test_fieldmodifier_multiple(self):
        self.assertNotEqual(
            SetField.from_str(str(t := SetField("", "f", set(SetField.SEPARATORS)))),
            t,
            msg="when values contain all separators, stringification shouldn't round-trip, but here it does!?",
        )

    def test_duration(self):
        for s, kw in {
            "10m": dict(minutes=10),
            "10m+2h": dict(minutes=10, hours=2),
            "2h 10m": dict(minutes=10, hours=2),
            "2h30m": dict(hours=2, minutes=30),
            "   1   w   2  days 3 hour  4 min 5 sec": dict(
                weeks=1, days=2, hours=3, minutes=4, seconds=5
            ),
        }.items():
            with self.subTest(string=s):
                self.assertEqual(
                    Token.from_str(s), Duration(string=s, duration=timedelta(**kw))
                )

    def test_from_string_roundtrip(self):
        for s in [
            "10:00",
            "until",
            "bla",
            "10min",
            "10m2h",
            "field=value",
            "field+=value",
            "field=",
            "field-=value",
            "tag+=until",
            "tag+=until,bla",
            "field+;=10:00;yesterday",
            "",
        ]:
            with self.subTest(string=s):
                token = Token.from_str(s)
                self.assertEqual(Token.from_str(str(token)), token)

    def test_from_strings(self):
        for input, (start, end) in {
            "10min ago": (dt.now() - td(minutes=10), None),
            "y10:00 - now": (today(hour=10) - days(1), dt.now()),
            "y10:00 until now": (today(hour=10) - days(1), dt.now()),
            "til 5min ago": (None, dt.now() - td(minutes=5)),
            "y10:00 until 10min ago": (
                today(hour=10) - days(1),
                dt.now() - td(minutes=10),
            ),
            "2h ago - now": (dt.now() - td(hours=2), dt.now()),
            "2h ago til 1h ago": (dt.now() - td(hours=2), dt.now() - td(hours=1)),
        }.items():
            with self.subTest(input=input):
                tokens = Token.from_strings(shlex.split(input), simplify=True)
                starttoken = next((t for t in tokens if isinstance(t, TimeStart)), None)
                endtoken = next((t for t in tokens if isinstance(t, TimeEnd)), None)
                self.assertEqual(
                    bool(starttoken),
                    bool(start),
                    msg=f"start should be {start} but is {starttoken}",
                )
                self.assertEqual(
                    bool(endtoken),
                    bool(end),
                    msg=f"end should be {end} but is {endtoken}",
                )
                if start:
                    self.assertTrue(
                        abs(starttoken.time - start).total_seconds() < 60,
                        msg=f"start should be {start} but is {starttoken.time}",
                    )
                if end:
                    self.assertTrue(
                        abs(endtoken.time - end).total_seconds() < 60,
                        msg=f"end should be {end} but is {endtoken.time}",
                    )


class EventTest(TestCase):
    def test_parse_date(self):
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
