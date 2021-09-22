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