from __future__ import annotations  # https://stackoverflow.com/a/33533514

# system modules
import re
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, fields, field
from datetime import datetime, datetime as dt, timedelta
from collections.abc import Sequence
from typing import Optional, Set, Dict, Union, List, Tuple, Iterator


logger = logging.getLogger(__name__)


@dataclass
class Token(ABC):
    string: str = field(compare=False)

    @classmethod
    def recursive_subclasses(cls):
        yield cls
        for subcls in cls.__subclasses__():
            yield from subcls.recursive_subclasses()

    @classmethod
    def from_str(cls, string: str) -> Union[Token, None]:
        """
        Recurse into subclasses and try their from_str() constructors.
        This exact method is inherited if it'string not overwritten (classmethods can't be abstractmethods...)
        """
        for subcls in cls.__subclasses__():
            if from_str := getattr(subcls, "from_str", None):
                try:
                    if token := from_str(string):
                        return token
                except Exception as e:
                    logger.error(f"Calling {from_str}({string!r}) didn't work: {e!r}")
        if cls is Token or str(cls) == str(Token):  # dirty hack: only in base class
            # fall back to just setting a tag
            return AddToField(string=string, field="tag", values=set([string]))
        return None

    @classmethod
    def from_strings(
        cls, strings: Sequence[str], simplify: bool = True
    ) -> Sequence[Union[Token | None]]:
        # first convert all strings to tokens
        tokens = [cls.from_str(s) for s in strings]
        if simplify:
            timetokens: List[TimeToken] = []
            othertokens: List[Union[Token | None]] = []
            # sort out the time-related tokens
            for token in tokens:
                if isinstance(token, TimeToken):
                    logger.debug(f"{token!r} is a TimeToken")
                    timetokens.append(token)
                else:
                    logger.debug(f"{token!r} is NOT a TimeToken")
                    othertokens.append(token)
            # interpret the time-related tokens
            # TODO: better catching of all combinations
            match timetokens:
                case [Time() as t] | [
                    TimeKeywordSince(),
                    Time() as t,
                ] | [
                    Time() as t,
                    TimeKeywordUntil(),
                ]:
                    othertokens.append(TimeStart(string="", time=t.time))
                case [
                    TimeKeywordUntil(),
                    Time() as t,
                ]:
                    othertokens.append(TimeEnd(string="", time=t.time))
                case [Time() as t1, Time() as t2] | [
                    Time() as t1,
                    TimeKeywordUntil(),
                    Time() as t2,
                ] | [
                    TimeKeywordSince(),
                    Time() as t1,
                    TimeKeywordUntil(),
                    Time() as t2,
                ]:
                    othertokens.append(TimeStart(string="", time=t1.time))
                    othertokens.append(TimeEnd(string="", time=t2.time))
                case [Duration() as d, TimeKeyword(name="ago")] | [
                    TimeKeywordSince(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    othertokens.append(TimeStart(string="", time=dt.now() - d.duration))
                case [
                    TimeKeywordUntil(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    othertokens.append(TimeEnd(string="", time=dt.now() - d.duration))
                case [
                    Time() as t,
                    TimeKeywordUntil(),
                    Duration() as d,
                    TimeKeyword(name="ago"),
                ]:
                    othertokens.append(TimeStart(string="", time=t.time))
                    othertokens.append(TimeEnd(string="", time=dt.now() - d.duration))
                case [
                    Duration() as d,
                    TimeKeyword(name="ago"),
                    TimeKeywordUntil(),
                    Time() as t,
                ]:
                    othertokens.append(TimeStart(string="", time=dt.now() - d.duration))
                    othertokens.append(TimeEnd(string="", time=t.time))
                case [
                    Duration() as d1,
                    TimeKeyword(name="ago"),
                    TimeKeywordUntil(),
                    Duration() as d2,
                    TimeKeyword(name="ago"),
                ]:
                    othertokens.append(
                        TimeStart(string="", time=dt.now() - d1.duration)
                    )
                    othertokens.append(TimeEnd(string="", time=dt.now() - d2.duration))
                case _:
                    logger.warning(
                        f"Don't know how to interpret time-related tokens {' '.join(t.string for t in timetokens)!r}. "
                        f"If you think this combination does makes sense, consider opening an issue (https://gitlab.com/nobodyinperson/annextimelog/-/issues/new) to discuss."
                    )
                    othertokens = tokens
            return othertokens
        else:
            return tokens

    @abstractmethod
    def __str__(self) -> str:
        pass


@dataclass
class Noop(Token):
    @classmethod
    def from_str(cls, string: str) -> Union[Noop, None]:
        if re.fullmatch(r"\s*", string):
            return cls(string=string)
        return None

    def __str__(self) -> str:
        return ""


@dataclass
class TimeToken(Token):
    pass


@dataclass
class TimeKeyword(TimeToken):
    name: str
    KEYWORDS = set("ago for in".split())

    @classmethod
    def from_str(cls, string: str) -> Union[TimeKeyword, None]:
        for subcls in cls.__subclasses__():
            if token := subcls.from_str(string):
                return token
        if string.lower() in cls.KEYWORDS:
            return cls(string=string, name=string)
        return None

    def __str__(self) -> str:
        return self.name


@dataclass
class TimeKeywordUntil(TimeKeyword):
    KEYWORDS = set("until til till to -".split())


@dataclass
class TimeKeywordSince(TimeKeyword):
    KEYWORDS = set("since starting from".split())


@dataclass
class Time(TimeToken):
    """
    A specification of a point in time, such as:

        10     # 10:00 today
        y10    # yesterday 10:00
        yy10   # day before yesterday 10:00
        t10    # tomorrow 10:00
        tt10   # day after tomorrow 10:00
        1500   # 15:00 today
        2023-12-30T13:13:40+0200    # full ISO format
        13:13:40 # partial full ISO format
        ...
    """

    time: datetime

    @classmethod
    def from_str(cls, string: str) -> Union[Time, None]:
        if string is None:
            return None
        offset = timedelta(days=0)
        if m := re.search(r"^(?P<prefix>[yt]+)(?P<rest>.*)$", string):
            offset = timedelta(
                days=sum(dict(y=-1, t=1).get(c, 0) for c in m.group("prefix"))
            )
            if string := m.group("rest"):
                pass
                # logger.debug(
                #     f"{string!r} starts with {m.group('prefix')!r}, so thats as an {offset = }"
                # )
            else:
                logger.debug(f"{string!r} means an {offset = } from today")
                return cls(
                    string=string,
                    time=dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    + offset,
                )
        if re.fullmatch(r"\d{3}", string):
            # prepend zero to '100', otherwise interpreted as 10:00
            string = f"0{string}"
        result = None
        todaystr = dt.now().strftime(todayfmt := "%Y-%m-%d")
        for i, f in enumerate(
            (
                lambda s: dt.now() if s == "now" else None,
                dt.fromisoformat,
                lambda s: dt.strptime(s, "%Y-%m"),
                lambda s: dt.strptime(s, "%Y/%m"),
                lambda s: dt.fromisoformat(f"{todaystr} {s}"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H%M"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H"),
                lambda s: dt.strptime(f"{todaystr} {s}", f"{todayfmt} %H:%M"),
                lambda s: dt.strptime(s, "%Y-%m-%d %H%M"),
            )
        ):
            try:
                if result := f(string):
                    break
            except Exception as e:
                pass
        if not result:
            return None
        result += offset
        return Time(string=string, time=result)

    def __str__(self) -> str:
        return self.time.strftime("%Y-%m-%dT%H:%M:%S%z")


@dataclass
class TimeStart(Time):
    # TODO: doesn't round-trip. But also doesn't need to.
    pass


@dataclass
class TimeEnd(Time):
    # TODO: doesn't round-trip. But also doesn't need to.
    pass


@dataclass
class Duration(TimeToken):
    """
    A duration specified in the following format:

        10min
        2h30m
        1week2days3hours4minutes5seconds
        1w2d3h4m5s
        ...
    """

    duration: timedelta

    UNITS = ["weeks", "days", "hours", "minutes", "seconds"]

    @classmethod
    def from_str(cls, string: str) -> Union[Duration, None]:
        durations: List[timedelta] = []
        matches: int = 0
        s = string
        while s:
            if m := re.match(
                rf"[^\da-z]*(?P<number>\d+)[^\da-z]*(?P<unit>[a-z]+)[^\da-z]*",
                s,
                flags=re.IGNORECASE,
            ):
                number, unit = m.groups()
                if kwarg := next(
                    (u for u in cls.UNITS if u.startswith(unit.lower())), None
                ):
                    durations.append(timedelta(**{kwarg: int(number)}))
                s = s[m.span()[-1] :]  # drop this match and go on
                continue
            else:
                return None
        if not durations:
            return None
        return cls(string=string, duration=sum(durations, start=timedelta(0)))

    def __str__(self) -> str:
        parts: List[Tuple[int, str]] = []
        duration = self.duration
        for unit in sorted(self.UNITS, key=lambda u: timedelta(**{u: 1}), reverse=True):
            unitdelta = timedelta(**{unit: 1})
            if abs(duration) < abs(unitdelta):
                continue
            unitblocks = duration // unitdelta
            parts.append((unitblocks, unit))
            duration -= unitblocks * unitdelta
        return "".join(f"{n}{u[0]}" for n, u in parts if n)


@dataclass
class FieldModifier(Token):
    """
    A metadata field modifier such as:

        field=value          # set 'field' to (only) 'value'
        field+=value         # add 'value' to 'field'
        field=bla,bli,blubb  # set 'field' to given three values
        field+=bla,bli,blubb # add multiple values to 'field'
        field-=value         # remove 'value' from 'field'
        field-=bla,bli,blubb # remove multiple values from 'field'
        field+/=a,b,c/d,e,f  # different separator (this adds 'a,b,c' and 'd,e,f' to 'field')
    """

    field: str

    # don't want to put too many in here, syntax might be needed later
    SEPARATORS = ",;:"

    @classmethod
    def from_str(cls, string) -> Union[FieldModifier, None]:
        # short form
        if m := re.search(r"^(?P<symbol>[@:=])(?P<value>.*)$", string.strip()):
            field = {"@": "location", ":": "note", "=": "title"}.get(
                m.group("symbol"), ""
            )
            return SetField(string=string, field=field, values=set([m.group("value")]))
        # long form
        if m := re.search(
            rf"(?P<field>\S+?)(?P<operator>[+-]?)(?P<sep>[{cls.SEPARATORS}]?)=(?P<values>.*)",
            string,
        ):
            field, operator, sep, values = m.groups()
            sep = sep or ","
            values = set(filter(bool, re.split(rf"(?:{re.escape(sep)})+", values)))
            if field.lower() in ["tags"]:
                # git annex uses field 'tag' for tags, for convenience adjust it here
                field = "tag"
            if operator.startswith("+"):
                return AddToField(string=string, field=field, values=values)
            elif operator.startswith("-"):
                return RemoveFromField(string=string, field=field, values=values)
            else:
                if values:
                    return SetField(string=string, field=field, values=values)
                else:
                    return UnsetField(string=string, field=field)
        return None


@dataclass
class FieldValueModifier(FieldModifier):
    values: Set[str]

    @property
    def separator(self) -> Union[str, None]:
        for sep in self.SEPARATORS:
            if not any(sep in v for v in self.values):
                return sep
        return None

    @property
    def values_joined(self) -> Tuple[str, str]:
        if sep := self.separator:
            return sep, sep.join(map(str.strip, self.values))
        else:
            it = iter(self.SEPARATORS)
            sep, repl = (next(it, "") for i in range(2))
            logger.warning(
                f"Don't know what separator to use for the values in {self!r}. "
                f"None of {self.SEPARATORS!r} is safe to use they're all present in the values and we don't have an escaping mechanism. "
                f"Falling back to {sep!r} and replacing all its occurrences with {repl!r}."
            )
            return sep, sep.join(v.replace(sep, repl).strip() for v in self.values)


@dataclass
class UnsetField(FieldModifier):
    def __str__(self) -> str:
        return f"{self.field}="


@dataclass
class SetField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}{sep if sep != ',' else ''}={joined}"


@dataclass
class AddToField(FieldValueModifier):
    def __str__(self):
        if (
            len(self.values) == 1
            and self.field.lower() in ["tag", "tags"]
            and isinstance(Token.from_str(value := next(iter(self.values))), AddToField)
        ):
            # shortcut for tags that are not interpreted as another token
            return f"{value}"
        else:
            sep, joined = self.values_joined
            return f"{self.field}+{sep if sep != ',' else ''}={joined}"


@dataclass
class RemoveFromField(FieldValueModifier):
    def __str__(self) -> str:
        sep, joined = self.values_joined
        return f"{self.field}-{sep if sep != ',' else ''}={joined}"
