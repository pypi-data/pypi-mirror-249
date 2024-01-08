# system modules
import math
import re
import json
import logging

# external modules
from rich.text import Text


logger = logging.getLogger(__name__)


GIT_CONFIG_REGEX = re.compile(r"^(?P<key>[^\s=]+)=(?P<value>.*)$", flags=re.IGNORECASE)


def pretty_duration(seconds):
    parts = dict()
    for unit, s in dict(d=24 * 60 * 60, h=60 * 60, m=60, s=1).items():
        parts[unit] = math.floor(seconds / s)
        seconds %= s
    colors = dict(d="green", h="blue", m="red", s="yellow")
    text = Text()
    for u, n in parts.items():
        if n:
            text.append(f"{n:2}").append(u, style=colors[u])
    return text


def from_jsonlines(string):
    if hasattr(string, "decode"):
        string = string.decode(errors="ignore")
    string = str(string or "")
    for i, line in enumerate(string.splitlines(), start=1):
        try:
            yield json.loads(line)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"line #{i} ({line!r}) is invalid JSON: {e!r}")
            continue
