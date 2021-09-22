import subprocess
import logging
from pathlib import Path
from typing import Any

from rich.logging import RichHandler
from rich import traceback

logger = logging.getLogger(__name__)


def cmd(command: str) -> str:
    logger.debug(f"Send cmd --> {command}")
    # Note: Ignoring unicode characters in SSIDs to prevent intermittent UnicodeDecodeErrors from occurring
    # while trying to connect to SSID when *any* AP is nearby that has unicode characters in the name
    response = (
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # type: ignore
        .stdout.read()
        .decode(errors="ignore")
    )
    logger.debug(f"Receive response --> {response}")

    return response


def setup_logging(output: Path) -> Any:
    global logger
    # Logging to file with millisecond timing
    fh = logging.FileHandler(output, mode="w")
    file_formatter = logging.Formatter(
        fmt="%(threadName)13s:%(asctime)s.%(msecs)03d %(filename)-26s %(lineno)4s %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    fh.setFormatter(file_formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Use Rich for colorful console logging
    sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
    stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
    sh.setFormatter(stream_formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    modules = ["pyflashcards.util", "pyflashcards.flashcards", "pyflashcards.flashcard_reader"]

    # Enable / disable logging in modules
    for module in modules:
        l = logging.getLogger(module)
        l.setLevel(logging.DEBUG)
        l.addHandler(fh)
        l.addHandler(sh)

    traceback.install()  # Enable exception tracebacks in rich logger

    return logger


# from https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
