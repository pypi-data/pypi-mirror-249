# system modules
import shlex
import logging
import subprocess
from pathlib import Path

# internal modules

# external modules
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.highlighter import ReprHighlighter, ISO8601Highlighter
from rich import box

logger = logging.getLogger(__name__)


def show_process_result(result, output_lexer="txt", show_title=None):
    table = Table(expand=True, padding=0, box=box.SIMPLE)
    if result.stdout:
        table.add_column("📢 STDOUT", ratio=1, justify="center")
    if result.stderr:
        table.add_column("⚠️  STDERR", ratio=1, justify="center")
    if not (result.stdout or result.stderr):
        table.add_column("*no output*")
    cols = []
    if result.stdout:
        cols.append(
            Syntax(
                result.stdout.rstrip(),
                lexer=output_lexer,
                line_numbers=True,
                word_wrap=True,
            )
        )
    if result.stderr:
        cols.append(
            Syntax(
                result.stderr.rstrip(),
                lexer="txt",
                line_numbers=True,
                word_wrap=True,
            )
        )
    if cols:
        table.add_row(*cols)

    if show_title or (
        show_title is None and logger.getEffectiveLevel() < logging.DEBUG - 10
    ):
        titleparts = [
            getattr(result, "title", None),
            f"(↩️  [b]return code {result.returncode}[/b])",
        ]
        if logger.getEffectiveLevel() > logging.DEBUG:
            titleparts.append(
                f"[code]{shlex.join(result.args)}[/code]",
            )
        table.title = "\n".join(filter(bool, titleparts))
    logger.console.print(Panel(table))


def run(
    runner,
    cmdline,
    return_error=True,
    title=None,
    output_lexer="txt",
    debug_on_error=True,
    stderr_is_error=True,
    **kwargs,
):
    """
    Run a given ``cmdline`` with a :mod:`subprocess` runner (e.g
    :any:`subprocess.check_output`) with passed command-line arguments.
    If ``return_error`` is ``True``, a raised
    :any:`subprocess.CalledProcessError` is caught and returned. If it's
    ``None``, just ``None`` is returned. Otherwise the exception is bubbled up.
    """
    cmdline = list(map(str, cmdline))
    if logger.getEffectiveLevel() < logging.DEBUG:
        lines = []
        if title:
            lines.append(f"# {title}")
        lines.append(
            f"""# 🚀 Executing (📋 you could copy-paste this) in 📁 {kwargs.get("cwd") or Path.cwd()}:"""
        )
        lines.append(shlex.join(cmdline))
        logger.console.print(
            Syntax(
                "\n".join(lines),
                "bash",
                line_numbers=False,
                indent_guides=False,
                word_wrap=True,
                padding=0,
            )
        )
    if runner is subprocess.run:
        kwargs.setdefault("capture_output", True)
        kwargs.setdefault("check", False)
    try:
        result = runner(
            cmdline, **{**dict(text=True, encoding="utf-8", errors="ignore"), **kwargs}
        )
    except subprocess.CalledProcessError as e:
        if return_error is True:
            return e
        elif return_error is None:
            return None
        else:
            raise
    result.title = title
    if (
        kwargs.get("capture_output") and logger.getEffectiveLevel() < logging.DEBUG - 5
    ) or (
        debug_on_error and (result.returncode or (result.stderr and stderr_is_error))
    ):
        if result.returncode or (result.stderr and stderr_is_error):
            logger.error(f"Something went wrong during {title or shlex.join(cmdline)}")
        show_process_result(result, output_lexer=output_lexer, show_title=True)
    return result


def get_repo_root(path=Path(".")):
    logger.debug(f"🔎 Finding where the containing git repo root is for path {path}")
    result = run(
        subprocess.run,
        ["git", "-C", Path(path), "rev-parse", "--show-toplevel"],
        title=f"find git repo root for {path}",
    )
    if result.returncode:
        return None
    return Path(result.stdout.rstrip("\n").rstrip("\r"))
