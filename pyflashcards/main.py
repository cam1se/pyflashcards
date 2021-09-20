import enum
import platform
import logging
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, List

from rich.logging import RichHandler
from rich import traceback
from gtts import gTTS

logger = logging.getLogger()

# TODO get this from gTTS
class SupportedLanguages(enum.Enum):
    ENGLISH = 'en'
    GREEK = 'el'

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

    traceback.install()  # Enable exception tracebacks in rich logger

    return logger

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


# TODO make singleton
class AudioPlayer:
    def __init__(self) -> None:
        os = None
        if (p:= platform.system().lower()) == "darwin":
            self.player = "afplay"
            os = "MacOS"
        else:
            raise NotImplementedError

        assert os is not None
        logger.debug(f"Using {self.player} to play audio on {os}")

    def play(self, word: str, language: SupportedLanguages) -> None:
        tts = gTTS(word, lang=language.value)
        # TODO put this in temp folder
        tts.save('temp.mp3')
        response = cmd(f"{self.player} temp.mp3")

@dataclass
class Flashcard:
    question: str
    answer: str
    keywords: List[str] = field(default_factory=list)
    language: SupportedLanguages = SupportedLanguages.ENGLISH

    def __post_init__(self):
        # Verify language
        assert self.language in SupportedLanguages
        self.player = AudioPlayer()

    def play_question(self):
        self.player.play(self.question, self.language)

    def play_answer(self):
        self.player.play(self.answer, self.language)



def main():
    setup_logging(Path("main.log"))

    flashcard1 = Flashcard(question="question",answer="answer")
    flashcard1.play_question()
    input()
    flashcard1.play_answer()

if __name__ == "__main__":
    main()