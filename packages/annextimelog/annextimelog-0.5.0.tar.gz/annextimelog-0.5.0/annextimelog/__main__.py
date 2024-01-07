# system modules
import time
import warnings
import unittest
import itertools
import glob
import collections
import uuid
import os
import json
import re
import textwrap
import sys
import shlex
import logging
import subprocess
import argparse
import datetime
from datetime import datetime as dt
from pathlib import Path

# internal modules
from annextimelog.event import Event
from annextimelog.log import stdout, stderr
from annextimelog.run import run, get_repo_root
from annextimelog import utils

# external modules
import rich
from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.pretty import Pretty
from rich.text import Text
from rich import box

logger = logging.getLogger(__name__)


def test_cmd_handler(args, other_args):
    loader = unittest.TestLoader()
    logger.debug(f"🧪 Importing test suite")
    import annextimelog.test

    logger.info(f"🚀 Running test suite")
    testsuite = loader.loadTestsFromModule(annextimelog.test)
    result = unittest.TextTestRunner(
        verbosity=args.test_verbosity, buffer=args.test_verbosity <= 2
    ).run(testsuite)
    logger.debug(f"{result = }")
    if result.wasSuccessful():
        logger.info(f"✅ Test suite completed successfully")
    else:
        logger.error(f"💥 There were problems during testing.")
        sys.exit(1)


def git_cmd_handler(args, other_args):
    result = run(subprocess.Popen, ["git", "-C", str(args.repo)] + other_args)
    result.wait()
    sys.exit(result.returncode)


def sync_cmd_handler(args, other_args):
    if logger.getEffectiveLevel() < logging.DEBUG:
        with run(
            subprocess.Popen, ["git", "-C", args.repo, "annex", "assist"]
        ) as process:
            process.wait()
            sys.exit(process.returncode)
    else:
        with stderr.status("Syncing..."):
            result = run(subprocess.run, ["git", "-C", args.repo, "annex", "assist"])
    if result.returncode or result.stderr:
        if result.returncode:
            logger.error(f"Syncing failed according to git annex.")
        if result.stderr:
            logger.warning(
                f"git annex returned some STDERR messages. "
                f"This might be harmless, maybe try again (a couple of times)."
            )
        sys.exit(1)
    else:
        logger.info(f"✅ Syncing finished")
    sys.exit(result.returncode)


def track_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    if not args.metadata:
        trackparser.print_help()
        sys.exit(2)
    event = Event.from_cli(args.metadata, args=args)
    if not (event.start and event.end):
        logger.critical(
            f"Currently, 'annextimelog track' can only record events with exactly two given time bounds. "
            f"This will change in the future."
        )
        sys.exit(1)
    if logger.getEffectiveLevel() < logging.DEBUG:
        logger.debug(f"Event before saving:")
        stderr.print(event.to_rich())
    # make the file
    event.store()
    cmd = ["git", "-C", args.repo, "annex", "metadata", "--key", event.key]
    for field, values in event.fields.items():
        for value in values:
            if hasattr(value, "strftime"):
                value = Event.timeformat(value)
            cmd.extend(["--set", f"{field}+={value}"])
    if run(subprocess.run, cmd).returncode:
        logger.error(
            f"Something went wrong setting annex metadata on event {event.id} key {event.key!r}"
        )
    if logger.getEffectiveLevel() <= logging.DEBUG and args.output_format not in (
        "rich",
        "console",
    ):
        logger.debug(f"Event after saving:")
        stderr.print(event.to_rich())
    event.output(args)


def summary_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    begin = getattr(args, "begin", None) or datetime.datetime.min
    end = getattr(args, "end", None) or datetime.datetime.max
    selected_period = next(
        (a for a in "day week month all".split() if getattr(args, a, None)),
        None,
    )
    match selected_period:
        case "day" | None:
            begin = max(
                begin, dt.now().replace(hour=0, minute=0, second=0, microsecond=1)
            )
            end = min(
                end,
                (dt.now() + datetime.timedelta(days=1)).replace(
                    hour=1, minute=1, second=1, microsecond=1
                ),
            )
        case "week":
            weekbegin = (
                t := dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
            ) - datetime.timedelta(days=t.weekday())
            if args.config.get("annextimelog.weekstartssunday") == "true":
                weekbegin -= datetime.timedelta(days=1)
            weekend = weekbegin + datetime.timedelta(days=7)
            begin = max(begin, weekbegin)
            end = min(end, weekend)
        case "month":
            monthbegin = dt(year=(t := dt.now()).year, month=t.month, day=t.day)
            monthend = monthbegin + datetime.timedelta(days=32)
            monthend = dt(year=monthend.year, month=monthend.month, day=1)
            begin = max(begin, monthbegin)
            end = min(end, monthend)
        case "all":
            pass  # no further constraints
        case _:
            warnings.warn("This should not happen.")
    logger.debug(f"{begin = }, {end = }")
    with logger.console.status(f"Querying metadata..."):
        # would be more elegant to use something like 'findkeys' which wouldn't output
        # duplicates, but then we'd have to use 'whereused' to find out the repo paths
        # and also 'findkeys' only lists existing non-missing annex keys, so meh...
        cmd = ["git", "-C", args.repo, "annex", "metadata", "--json"]
        cmd.extend(
            L := Event.git_annex_args_timerange(
                start=None if begin == datetime.datetime.min else begin,
                end=None if end == datetime.datetime.max else end,
            )
        )
        logger.debug(f"git annex matching args: {L = }")
        result = run(subprocess.run, cmd)
    for event in Event.multiple_from_metadata(
        utils.from_jsonlines(result.stdout), args=args
    ):
        event.output(args)


def delete_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"🙈 Ignoring other arguments {other_args}")
    result = run(
        subprocess.run,
        ["git", "-C", args.repo, "ls-files"] + [f"*{p}*" for p in args.patterns],
    )
    gitpaths = set(Path(p) for p in result.stdout.splitlines())
    logger.debug(f"{gitpaths = }")
    globpaths = set(
        p.relative_to(args.repo)
        for p in itertools.chain.from_iterable(
            args.repo.glob(f"**/*{pattern}*") for pattern in args.patterns
        )
        if (args.repo / ".git") not in p.parents
    )
    logger.debug(f"{globpaths = }")
    paths = gitpaths.union(globpaths)
    if not paths:
        logger.error(
            f"🤷 No events found for id patterns {args.patterns}. "
            "(Remember patterns are case-sensitive!)"
        )
        sys.exit(1)
    ids = set(p.stem for p in paths)
    if len(ids) > 1 and not args.force:
        logger.error(
            f"{len(ids)} events found matching patterns {' '.join(map(repr,args.patterns))}: {ids}. "
            f"Use 'atl --force del ...' to delete all of them."
        )
        sys.exit(1)
    logger.info(f"Matched events: {ids}")
    result = run(subprocess.run, ["git", "-C", args.repo, "rm", "-rf"] + sorted(paths))
    success = not (result.returncode or result.stderr)
    if args.config.get("annextimelog.commit", "true") == "true":
        result = run(
            subprocess.run,
            [
                "git",
                "-C",
                args.repo,
                "commit",
                "-m",
                f"🗑️ Remove event {args.patterns!r}",
            ],
        )
        success |= not (result.returncode or result.stderr)
    if success:
        logger.info(f"🗑️ Removed {len(paths)} paths for events {ids}")
    else:
        logger.error(f"Couldn't remove events {ids}")
        sys.exit(1)


def key2value(x):
    if m := utils.GIT_CONFIG_REGEX.fullmatch(x):
        return m.groups()
    else:
        raise argparse.ArgumentTypeError(f"{x!r} is not a key=value pair")


parser = argparse.ArgumentParser(
    description="⏱️ Time tracker based on Git Annex",
    prog="annextimelog",
    formatter_class=argparse.RawTextHelpFormatter,
)

datagroup = parser.add_argument_group(title="Data")
datagroup.add_argument(
    "--repo",
    type=Path,
    default=(
        default := Path(
            os.environ.get("ANNEXTIMELOGREPO")
            or os.environ.get("ANNEXTIMELOG_REPO")
            or Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
            / "annextimelog"
        )
    ),
    help=f"Backend repository to use. "
    f"Defaults to $ANNEXTIMELOGREPO, $ANNEXTIMELOG_REPO or $XDG_DATA_HOME/annextimelog (currently: {str(default)})",
)

parser.add_argument(
    "--force",
    action="store_true",
    help="Just do it. Ignore potential data loss.",
)
parser.add_argument(
    "--no-config",
    action="store_true",
    help="Ignore config from git",
)
parser.add_argument(
    "-c",
    dest="extra_config",
    action="append",
    metavar="key=value",
    type=key2value,
    help="Set a temporary config key=value. "
    "If not present, 'annextimelog.' will be prepended to the key.",
    default=[],
)

outputgroup = parser.add_argument_group(
    title="Output", description="Options changing output behaviour"
)
outputgroup.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
outputgroup.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)
outputgroup.add_argument(
    "-O",
    "--output-format",
    choices={"rich", "console", "json", "timeclock", "cli"},
    default=(default := "console"),  # type: ignore
    help=f"Select output format. Defaults to {default!r}.",
)


subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")
testparser = subparsers.add_parser(
    "test",
    help="run test suite",
    description="Run the test suite",
    formatter_class=argparse.RawTextHelpFormatter,
)
testparser.add_argument(
    "-v",
    "--verbose",
    dest="test_verbosity",
    help="Increase verbosity of test runner. "
    "-v: show test names, "
    "-vv: show raw debug output in all tests, not just failed tests",
    action="count",
    default=1,
)
testparser.set_defaults(func=test_cmd_handler)
gitparser = subparsers.add_parser(
    "git",
    help="Access the underlying git repository",
    add_help=False,
    formatter_class=argparse.RawTextHelpFormatter,
)
gitparser.set_defaults(func=git_cmd_handler)
syncparser = subparsers.add_parser(
    "sync",
    help="sync data",
    description=textwrap.dedent(
        """
    Sync data with configured remotes.
    """
    ).strip(),
    aliases=["sy"],
)
syncparser.set_defaults(func=sync_cmd_handler)
trackparser = subparsers.add_parser(
    "track",
    help="record a time period",
    description=textwrap.dedent(
        """
    Record a time with metadata.

    Example:

    > atl tr y22  800 work python @GUZ ="annextimelog dev" :"working on cli etc." project=herz project+=co2

    """
    ).strip(),
    aliases=["tr"],
    formatter_class=argparse.RawTextHelpFormatter,
)
trackparser.add_argument(
    "metadata",
    nargs="*",
    help=textwrap.dedent(
        """
    Examples:

        10:00                   10:00 today
        y15:00                  15:00 yesterday
        yy15:00                 15:00 the day before yesterday
        t20:00                  20:00 tomorrow
        tt20:00                 20:00 the day after tomorrow
        2023-12-04T
        justaword               adds tag 'justaword'
        "with space"            (shell-quoted) adds tag "with space"
        field=value             sets metadata field 'field' to (only) 'value'
        field+=value            adds 'value' to metadata field
"""
    ).strip(),
)
trackparser.set_defaults(func=track_cmd_handler)
deleteparser = subparsers.add_parser(
    "delete",
    help="delete an event",
    description=textwrap.dedent(
        """
    Delete an event.

    Example:

    # the following commands would delete event 3QicA4G4
    > atl del 3QicA4G4
    > atl del 3Qi
    > atl del A4

    """
    ).strip(),
    aliases=["del", "rm", "remove"],
    formatter_class=argparse.RawTextHelpFormatter,
)
deleteparser.add_argument(
    "patterns",
    nargs="+",
    metavar="ID",
    help="case-sensitive glob patterns matching the IDs to delete. "
    "Use 'atl su ...' to find the IDs. "
    "Use 'atl --force del ...' to delete multiple matching events.",
)
deleteparser.set_defaults(func=delete_cmd_handler)
summaryparser = subparsers.add_parser(
    "summary",
    help="show a summary of tracked periods",
    description=textwrap.dedent(
        """
    List a summary of tracked periods

    """
    ).strip(),
    aliases=["su", "ls", "list"],
    formatter_class=argparse.RawTextHelpFormatter,
)
periodgroup = summaryparser.add_mutually_exclusive_group()
periodgroup.add_argument("-d", "--day", action="store_true")
periodgroup.add_argument("-w", "--week", action="store_true")
periodgroup.add_argument("-m", "--month", action="store_true")
periodgroup.add_argument("-a", "--all", action="store_true")
summaryparser.add_argument(
    "-b", "--begin", metavar="report beginning time", type=Event.parse_date
)
summaryparser.add_argument(
    "-e", "--end", metavar="report end time", type=Event.parse_date
)
summaryparser.add_argument("-l", "--long", action="store_true", help="more details")
summaryparser.set_defaults(func=summary_cmd_handler)


def cli(args=None):
    args, other_args = parser.parse_known_args(args=args)

    logging.basicConfig(
        level=(level := logging.INFO - (args.verbose - args.quiet) * 5),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=stderr,  # log to stderr
                rich_tracebacks=True,
                show_path=level < logging.DEBUG - 10,
            )
        ],
    )
    logger.debug(f"{args = }")
    logger.debug(f"{other_args = }")

    if args.repo.exists() and not args.repo.is_dir():
        logger.critical(f"{args.repo} exists but is not a directory.")
        sys.exit(1)

    if args.repo.exists():
        logger.debug(f"{args.repo} exists")
        if repo_root := get_repo_root(args.repo):
            if repo_root.resolve() != args.repo.resolve():
                logger.critical(
                    f"There's something funny with {args.repo}: git says the repo root is {repo_root}. "
                )
                sys.exit(1)
        else:
            logger.critical(f"{args.repo} exists but is no git repository. 🤔")
            sys.exit(1)
    else:
        if not args.repo.parent.exists():
            logger.info(f"📁 Creating {args.repo.parent}")
            args.repo.parent.mkdir(parent=True, exist_ok=True)
        logger.info(f"Making a git repository at {args.repo}")
        result = run(
            subprocess.run, ["git", "init", str(args.repo)], capture_output=True
        )
        if result.returncode:
            logger.error(f"Couldn't make git repository at {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git repository

    logger.debug(f"Reading config from repo {args.repo}")
    result = run(subprocess.run, ["git", "-C", args.repo, "config", "--list"])
    args.config = dict()
    for line in result.stdout.splitlines():
        if m := utils.GIT_CONFIG_REGEX.fullmatch(line):
            args.config[m.group("key")] = m.group("value")
    if logger.getEffectiveLevel() < logging.DEBUG - 5:
        logger.debug(f"Read git config:\n{args.config}")
    if args.no_config:
        args.config = {k: v for k, v in args.config.items() if k in ["annex.uuid"]}
    args.config.update(
        {
            re.sub(r"^(annextimelog\.)?", "annextimelog.", k): v
            for k, v in args.extra_config
        }
    )
    if logger.getEffectiveLevel() < logging.DEBUG - 5:
        logger.debug(f"Config:\n{args.config}")

    logger.debug(f"Making sure {args.repo} is a git annex repository")
    if not args.config.get("annex.uuid"):
        logger.debug(f"{args.repo} is not a git annex repository")
        if not (
            result := run(
                subprocess.run,
                ["git", "-C", args.repo, "annex", "init"],
                title=f"add an annex to {args.repo}",
            )
        ).returncode:
            logger.info(f"Added an annex to {args.repo}")
        else:
            logger.critical(f"Couldn't add an annex to {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git annex repository

    if args.config.get("annextimelog.commit", "true") == "true":
        if args.subcommand not in ["git"]:
            result = run(
                subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
            )
            if result.returncode or result.stdout or result.stderr:
                logger.warning(
                    f"🐛 The repo {args.repo} is not clean. "
                    f"This should not happen. Committing away the following changes:"
                )
                result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])
                with logger.console.status("Committing..."):
                    result = run(
                        subprocess.run, ["git", "-C", args.repo, "annex", "add"]
                    )
                    result = run(subprocess.run, ["git", "-C", args.repo, "add", "-A"])
                    result = run(
                        subprocess.run,
                        ["git", "-C", args.repo, "commit", "-m", "🧹 Leftover changes"],
                    )
                result = run(
                    subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
                )
                if not (result.returncode or result.stderr):
                    logger.info(f"✅ Repo is now clean")
                else:
                    logger.warning(f"Commiting leftover changes didn't work.")

    # handle the subcommand
    # (when a subcommand is specified, the 'func' default is set to a callback function)
    if not getattr(args, "func", None):
        # default to 'atl summary'
        args.func = summary_cmd_handler
    try:
        args.func(args, other_args)
    finally:
        if (
            args.subcommand not in ["git"]
            and args.config.get("annextimelog.commit", "true") == "true"
        ):
            result = run(
                subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"]
            )
            if result.returncode or result.stdout or result.stderr:
                logger.warning(
                    f"🐛 This command left the repo {args.repo} in an unclean state. "
                    f"This should not happen. Consider investigating. "
                    f"The next time you run any 'annextimelog' command, these changes will be committed."
                )
                result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])


if __name__ == "__main__":
    cli()
