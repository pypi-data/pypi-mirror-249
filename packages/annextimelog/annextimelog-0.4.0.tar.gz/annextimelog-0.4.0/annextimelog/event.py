# system modules
import re
import sys
import json
from argparse import Namespace
import copy
import shlex
import subprocess
import locale
import logging
import textwrap
import collections
import string
import random
import datetime
from datetime import datetime as dt
from pathlib import Path
from dataclasses import dataclass, asdict, fields
from typing import Optional, Set, Dict
from zoneinfo import ZoneInfo

# internal modules
from annextimelog.run import run
from annextimelog.log import stdout
from annextimelog import utils

# external modules
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.highlighter import ReprHighlighter, ISO8601Highlighter
from rich import box

logger = logging.getLogger(__name__)


@dataclass(repr=False)
class Event:
    args: Optional[Namespace] = None
    id: Optional[str] = None
    paths: Optional[Set[Path]] = None
    key: Optional[str] = None
    fields: Optional[Dict[str, Set[str]]] = None

    SUFFIX = ".ev"

    def __post_init__(self):
        if self.id is None:
            self.id = self.random_id()
        if self.paths is None:
            self.paths = set()
        if self.fields is None:
            self.fields = collections.defaultdict(set)
        if self.args is None:
            self.args = Namespace()

    @property
    def location(self):
        if "location" not in self.fields:
            self.fields["location"] = set()
        return self.fields["location"]

    @property
    def start(self):
        if "start" not in self.fields:
            self.fields["start"] = set()
        if not (start := self.fields["start"]):
            return None
        elif len(start) > 1:
            try:
                earliest = min(
                    d.astimezone() for d in (self.parse_date(s) for s in start) if d
                )
            except Exception as e:
                logger.error(
                    f"There are {len(start)} start times for event {self.id!r}, but I can't determine the earliest: {e!r}"
                )
                self.fields["start"].clear()
                return None
            logger.warning(
                f"There were {len(start)} start times for event {self.id!r}. Using the earlier one {earliest}."
            )
            self.fields["start"].clear()
            self.fields["start"].add(earliest)
        return self.parse_date(next(iter(self.fields["start"]), None))

    @start.setter
    def start(self, value):
        if value is None:
            self.fields["start"].clear()
            return
        if d := self.parse_date(value):
            self.fields["start"].clear()
            self.fields["start"].add(d)
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["start"].clear()

    @property
    def end(self):
        if "end" not in self.fields:
            self.fields["end"] = set()
        if not (end := self.fields["end"]):
            return None
        elif len(end) > 1:
            try:
                latest = min(
                    d.astimezone() for d in (self.parse_date(s) for s in end) if d
                )
            except Exception as e:
                logger.error(
                    f"There are {len(end)} end times for event {self.id!r}, but I can't determine the latest: {e!r}"
                )
                self.fields["end"].clear()
                return None
            logger.warning(
                f"There were {len(end)} end times for event {self.id!r}. Using the later one {latest}."
            )
            self.fields["end"].clear()
            self.fields["end"].add(latest)
        return self.parse_date(next(iter(self.fields["end"]), None))

    @end.setter
    def end(self, value):
        if value is None:
            self.fields["end"].clear()
            return
        if d := self.parse_date(value):
            self.fields["end"].clear()
            self.fields["end"].add(d)
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["end"].clear()

    @property
    def note(self):
        if len(note := self.fields.get("note", set())) > 1:
            note = "\n".join(self.fields["note"])
            self.fields["note"].clear()
            self.fields["note"].add(note)
        return "\n".join(self.fields.get("note", set()))

    @note.setter
    def note(self, value):
        self.fields["note"].clear()
        self.fields["note"].add(value)

    @property
    def title(self):
        if len(title := self.fields.get("title", set())) > 1 or any(
            re.search(r"[\r\n]", t) for t in title
        ):
            title = " ".join(re.sub(r"[\r\n]+", " ", t) for t in self.fields["title"])
            self.fields["title"].clear()
            self.fields["title"].add(title)
        return "\n".join(self.fields.get("title", set()))

    @title.setter
    def title(self, value):
        value = re.sub(r"[\r\n]+", " ", str(value))
        self.fields["title"].clear()
        self.fields["title"].add(value)

    @property
    def tags(self):
        if "tag" not in self.fields:
            self.fields["tag"] = set()
        return self.fields["tag"]

    @classmethod
    def multiple_from_metadata(cls, data, **init_kwargs):
        keys = collections.defaultdict(lambda: collections.defaultdict(set))
        for i, data in enumerate(data, start=1):
            if logger.getEffectiveLevel() < logging.DEBUG - 5:
                logger.debug(f"parsed git annex metadata line #{i}:\n{data}")
            if key := data.get("key"):
                keys[key]["data"] = data
            if p := next(iter(data.get("input", [])), None):
                keys[key]["paths"].add(p)
        for key, info in keys.items():
            if not (data := info.get("data")):
                continue
            event = Event.from_metadata(data, paths=info["paths"], **init_kwargs)
            if logger.getEffectiveLevel() < logging.DEBUG - 5:
                logger.debug(f"parsed Event from metadata line #{i}:\n{event}")
            yield event

    def clean(self):
        """
        Remove inconsistencies in this event.
        """
        properties = [
            attr
            for attr in dir(self)
            if isinstance(getattr(type(self), attr, None), property)
        ]
        # Call all properties - they do their own cleanup
        for p in properties:
            getattr(self, p)
        # remove empty fields
        for field in (empty_fields := [f for f, v in self.fields.items() if not v]):
            del self.fields[field]

    @staticmethod
    def random_id():
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def parse_date(string):
        if isinstance((d := string), datetime.datetime):
            return d
        if string is None:
            return None
        offset = datetime.timedelta(days=0)
        if m := re.search(r"^(?P<prefix>[yt]+)(?P<rest>.*)$", string):
            offset = datetime.timedelta(
                days=sum(dict(y=-1, t=1).get(c) for c in m.group("prefix"))
            )
            if string := m.group("rest"):
                logger.debug(
                    f"{string!r} starts with {m.group('prefix')!r}, so thats as an {offset = }"
                )
            else:
                logger.debug(f"{string!r} means an {offset = } from today")
                return (
                    dt.now().replace(hour=0, minute=0, second=0, microsecond=0) + offset
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
        if result:
            result += offset
        return result

    @classmethod
    def git_annex_args_timerange(cls, start=None, end=None):
        """
        Construct a git-annex matching expression suitable for use as arguments with :any:$(subprocess.run) to only match data files containing data in a given period of time based on the unix timestamp in the 'start' and 'end' metadata
        """
        data_starts_before_end_or_data_ends_after_start = shlex.split(
            "-( --metadata start<{end} --or --metadata end>{start} -)"
        )
        data_not_only_before_start = shlex.split(
            "--not -( --metadata start<{start} --and --metadata end<{start} -)"
        )
        data_not_only_after_end = shlex.split(
            "--not -( --metadata start>{end} --and --metadata end>{end} -)"
        )
        condition = []
        info = dict()
        start = Event.parse_date(start)
        end = Event.parse_date(end)
        if start is not None:
            condition += data_not_only_before_start
            info["start"] = cls.timeformat(start)
        if end is not None:
            condition += data_not_only_after_end
            info["end"] = cls.timeformat(end)
        if all(x is not None for x in (start, end)):
            condition += data_starts_before_end_or_data_ends_after_start
        return [p.format(**info) for p in condition]

    @staticmethod
    def timeformat(t, timezone=ZoneInfo("UTC")):
        return t.astimezone(timezone).strftime("%Y-%m-%dT%H:%M:%S%z")

    def store(self, args=None):
        args = args or self.args
        if not getattr(args, "repo", None):
            raise ValueError(
                f"Cannot store() and Event without knowing what repo it belongs to. "
                "No args given and the event's args don't contain a repo."
            )
        self.start = self.start or datetime.date.now()
        self.end = self.end or datetime.date.now()
        if self.end < self.start:
            logger.info(
                f"↔️  event {self.id!r}: Swapping start and end (they're backwards)"
            )
            self.start, self.end = self.end, self.start

        def folders():
            start, end = self.start, self.end
            start = datetime.date(start.year, start.month, start.day)
            end = datetime.date(end.year, end.month, end.day)
            day = start
            lastweekpath = None
            while day <= end:
                path = Path()
                for p in "%Y %m %d".split():
                    path /= day.strftime(p)
                yield path
                weekpath = Path()
                for p in "%Y W %W".split():
                    weekpath /= day.strftime(p)
                if weekpath != lastweekpath:
                    yield weekpath
                lastweekpath = weekpath
                day += datetime.timedelta(days=1)

        paths = set()
        for folder in folders():
            if not (folder_ := self.args.repo / folder).exists():
                logger.debug(f"📁 Creating new folder {folder}")
                folder_.mkdir(parents=True)
            file = (folder_ / self.id).with_suffix(self.SUFFIX)
            if (file.exists() or file.is_symlink()) and not (self.paths or self.key):
                logger.warning(
                    f"🐛 {file} exists although this event {event.id} is new (it has no paths or key attached). "
                    f"This is either a bug 🐛 or you just witnessed a collision. 💥"
                    f"🗑️ Removing {file}."
                )
                file.unlink()
            if file.is_symlink() and not os.access(str(file), os.W_OK):
                logger.debug(f"🗑️ Removing existing read-only symlink {file}")
                file.unlink()
            file_existed = file.exists()
            with file.open("w") as fh:
                logger.debug(
                    f"🧾 {'Overwriting' if file_existed else 'Creating'} {file} with content {self.id!r}"
                )
                fh.write(self.id)
            try:
                paths.add(file.relative_to(self.args.repo))
            except ValueError:
                paths.add(file)
        if obsolete_paths := self.paths - paths:
            logger.debug(
                f"{len(obsolete_paths)} paths for event {self.id!r} are now obsolete:"
                f"\n{chr(10).join(map(str(obsolete_paths)))}"
            )
            result = run(
                subprocess.run,
                ["git", "-C", self.args.repo, "rm", "-rf"] + obsolete_paths,
            )
        self.paths = paths
        with logger.console.status(f"Adding {len(self.paths)} paths..."):
            result = run(
                subprocess.run,
                ["git", "-C", self.args.repo, "annex", "add", "--json"]
                + sorted(self.paths),
                output_lexer="json",
                title=f"Adding {len(self.paths)} paths for event {self.id!r}",
            )
            keys = set()
            for info in utils.from_jsonlines(result.stdout):
                if key := info.get("key"):
                    keys.add(key)
            if len(keys) != 1:
                logger.warning(
                    f"🐛 Adding {len(self.paths)} paths for event {self.id!r} resulted in {len(keys)} keys {keys}. "
                    f"That should be exactly 1. This is probably a bug."
                )
            if keys:
                self.key = next(iter(keys), None)
                logger.debug(f"🔑 key for event {self.id!r} is {self.key!r}")
        if args.config.get("annextimelog.fast", "false") != "true":
            with logger.console.status(f"Force-dropping {keys = }..."):
                result = run(
                    subprocess.run,
                    ["git", "-C", self.args.repo, "annex", "drop", "--force", "--key"]
                    + list(keys),
                    title=f"Force-dropping {keys = } for event {self.id!r}",
                )
        if args.config.get("annextimelog.commit", "true") == "true":
            with logger.console.status(f"Committing addition of event {self.id!r}..."):
                result = run(
                    subprocess.run,
                    [
                        "git",
                        "-C",
                        self.args.repo,
                        "commit",
                        "-m",
                        f"➕ Add {self.id!r} ({self.title or 'untitled'})",
                    ],
                    title=f"Committing addition of event {self.id!r}",
                )
                if not result.returncode:
                    logger.info(f"✅ Committed addition of event {self.id!r}")

    #################
    ### 📥  Input ###
    #################
    @classmethod
    def from_metadata(cls, data, **init_kwargs):
        """
        Create an event from a parsed output line of ``git annex metadata --json``.
        """
        path = Path(data.get("input", [None])[0])
        fields = data.get("fields", dict())
        kwargs = init_kwargs.copy()
        kwargs.setdefault("paths", set())
        kwargs["paths"].add(path)
        kwargs.update(
            dict(
                id=path.stem,
                key=data.get("key"),
                fields={
                    k: set(v)
                    for k, v in fields.items()
                    if not (k.endswith("-lastchanged") or k in ["lastchanged"])
                },
            )
        )
        return cls(**kwargs)

    @classmethod
    def from_cli(cls, cliargs, **kwargs):
        """
        Create a new event from command-line arguments such as given to 'atl track'
        """
        event = cls(**kwargs)
        for i, arg in enumerate(cliargs, start=1):
            if re.fullmatch(r"\s*", arg):
                logger.debug(f"Ignoring empty argument #{i} ({arg!r})")
                continue
            if t := Event.parse_date(arg):
                logger.debug(
                    f"Interpreted argument #{i} {arg!r} as {Event.timeformat(t)}"
                )
                if event.start is None:
                    event.start = t
                elif event.end is None:
                    event.end = t
                else:
                    logger.warning(
                        f"Ignoring argument #{i} {arg!r}. "
                        f"Looks like a time but we already have two times {event.start = }, {event.end = }."
                    )
                continue
            if m := re.search(r"^@(.*)$", arg.strip()):
                location = m.group(1).strip()
                logger.debug(f"argument #{i} {arg!r} means {location = !r}")
                event.location.add(location)
                continue
            if m := re.search(r"^:(.*)$", arg.strip()):
                note = m.group(1).strip()
                logger.debug(f"argument #{i} {arg!r} is a note {note = !r}")
                if event.note:
                    logger.warning(f"Overwriting previous note {note!r}")
                event.note = note
                continue
            if m := re.search(r"^=(.*)$", arg.strip()):
                title = m.group(1).strip()
                logger.debug(f"argument #{i} {arg!r} is a {title = !r}")
                if event.title:
                    logger.warning(f"Overwriting previous title {title!r}")
                event.title = title
                continue
            if m := re.search(r"(?P<field>\S+?)(?P<operator>[+-]?)=(?P<value>.*)", arg):
                field, operator, value = m.groups()
                if operator.startswith("+"):
                    logger.debug(
                        f"argument #{i} {arg!r} adds {value!r} to metadata field {field!r}"
                    )
                    event.fields[field].add(value)
                elif operator.startswith("-"):
                    logger.debug(
                        f"argument #{i} {arg!r} removes {value!r} from metadata field {field!r}"
                    )
                    if arg in (values := event.fields[field]):
                        values.remove(arg)
                else:
                    logger.debug(
                        f"argument #{i} {arg!r} sets metadata field {field!r} to (only) {value!r}"
                    )
                    event.fields[field] = {value}
                continue
            logger.debug(f"argument #{i} {arg!r} is a tag")
            event.tags.add(arg)
        event.clean()
        return event

    ##################
    ### 📢  Output ###
    ##################
    def to_rich(self, long=None):
        table = Table(title=self.title, padding=0, box=box.ROUNDED, show_header=False)
        table.add_column("", justify="left")
        table.add_column("Field", justify="right", style="cyan")
        table.add_column("Value", justify="left")
        if self.id:
            table.add_row("💳", "id", f"[b]{self.id}[/b]")
        if self.paths and (getattr(self.args, "long", None) or long is True):
            table.add_row(
                "🧾",
                "paths",
                ReprHighlighter()(Text("\n".join(str(p) for p in self.paths))),
            )
        if self.paths and (getattr(self.args, "long", None) or long is True):
            table.add_row("🔑", "key", self.key)
        timehighlighter = ISO8601Highlighter()
        if start := self.start:
            table.add_row("🚀", "start", start.astimezone().strftime("%c%Z"))
        if end := self.end:
            table.add_row("⏱️", "end", end.astimezone().strftime("%c%Z"))
        if start and end:
            table.add_row(
                "⌛", "duration", utils.pretty_duration((end - start).total_seconds())
            )
        if self.location:
            table.add_row(
                "📍", "location", ", ".join([f"📍 {t}" for t in sorted(self.location)])
            )
        if self.tags:
            table.add_row(
                "🏷️", "tags", " ".join([f"🏷️ {t}" for t in sorted(self.tags)])
            )
        for field, values in self.fields.items():
            if field in "start end tag location title note".split():
                continue
            table.add_row("", field, " ".join(f"📝 {value}" for value in values))
        if self.note:
            table.add_row("📝", "note", self.note)
        return table

    def to_dict(self):
        if sys.version_info < (3, 12):
            # https://github.com/python/cpython/pull/32056
            # dataclasses.asdict() doesn't like defaultdict
            e = copy.copy(self)
            e.fields = dict(self.fields)  # turn defaultdict into plain dict
        else:
            e = self
        return asdict(e)

    def to_json(self):
        def default(x):
            if hasattr(x, "strftime"):
                return self.timeformat(x)
            if not isinstance(x, str):
                try:
                    iter(x)
                    return tuple(x)
                except TypeError:
                    pass
            return str(x)

        return json.dumps(self.to_dict(), default=default)

    def to_timeclock(self):
        def sanitize(s):
            s = re.sub(r"[,:;]", r"⁏", s)  # replace separation chars
            s = re.sub(r"[\r\n]+", r" ", s)  # no newlines
            return s

        hledger_tags = {
            k: " ⁏ ".join(map(sanitize, v))
            for k, v in self.fields.items()
            if k not in "start end".split()
        }
        for tag in sorted(self.tags):
            hledger_tags[tag] = ""
        hledger_tags = [f"{t}: {v}" for t, v in hledger_tags.items()]
        hledger_comment = f";  {', '.join(hledger_tags)}" if hledger_tags else ""
        info = [
            ":".join(self.fields.get("account", self.tags)),
            self.title,
            hledger_comment,
        ]
        return textwrap.dedent(
            f"""
        i {self.start.strftime('%Y-%m-%d %H:%M:%S%z')} {'  '.join(filter(bool,info))}
        o {self.end.strftime('%Y-%m-%d %H:%M:%S%z')}
        """
        ).strip()

    def to_cli(self):
        args = []
        fields = self.fields.copy()
        if start := self.start:
            fields.pop("start", None)
            args.append(self.timeformat(start, timezone=None))
        if end := self.end:
            fields.pop("end", None)
            args.append(self.timeformat(end, timezone=None))
        if tags := fields.pop("tag", None):
            args.extend(tags)
        for field, values in fields.items():
            for value in values:
                if hasattr(value, "strftime"):
                    value = Event.timeformat(value, timezone=None)
                args.append(f"{field}+={value}")
        return args

    def output(self, args):
        printer = {
            "timeclock": print,
            "json": print,
            "cli": lambda args: print(shlex.join(["atl", "tr"] + self.to_cli())),
        }.get(args.output_format, stdout.print)
        printer(getattr(self, f"to_{args.output_format}", self.to_rich)())

    def __repr__(self):
        if hasattr(sys, "ps1"):
            with (c := Console()).capture() as capture:
                c.print(self.to_rich(long=True))
            return capture.get()
        else:
            args = ", ".join(
                (
                    f"{f.name}=..."
                    if f.name in "args".split()
                    else f"{f.name}={getattr(self,f.name)!r}"
                )
                for f in fields(self)
            )
            return f"{self.__class__.__name__}({args})"

    def __eq__(self, other):
        """
        Two events are considered equal if their fields match sensibly
        """

        def sanitize(fields):
            return {
                k: (set([v]) if isinstance(v, str) else set(v))
                for k, v in fields.items()
                if v
            }

        fields = sanitize(self.fields)
        otherfields = sanitize(other.fields)
        for field, values in fields.items():
            othervalues = otherfields.pop(field, None)
            if not (values or othervalues):  # both empty
                continue
            if values != othervalues:
                return False
        if any(otherfields.values()):
            return False
        return True
