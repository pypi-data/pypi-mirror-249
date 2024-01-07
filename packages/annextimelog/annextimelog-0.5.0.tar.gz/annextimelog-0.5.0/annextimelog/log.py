# system modules
import logging
import locale

# external modules
from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)

# Allow locale for strftime etc.
locale.setlocale(locale.LC_ALL, "")


def logger_console_getter(logger):
    for handler in logger.root.handlers:
        if console := getattr(handler, "console", None):
            logger._console = console
            return console
    return Console(stderr=True)  # last resort: make temporary new one


# monkey-patch Logger to have a 'console' property returning the actually used
# console in the RichHandler
logging.Logger.console = property(logger_console_getter)  # type: ignore
