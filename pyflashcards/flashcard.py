from enum import Enum
import platform
from pathlib import Path
from dataclasses import InitVar, dataclass, field
from typing import List, Optional, Any
import logging

from rich.console import Console
from gtts import gTTS
import vlc

from pyflashcards.util import cmd

logger = logging.getLogger(__name__)


class OperatingSystems(Enum):
    MACOS = "darwin"
    WINDOWS = "windows"


# TODO get this from gTTS
class SupportedLanguages(Enum):
    ENGLISH = "english"
    GREEK = "greek"


language_mapping = {
    SupportedLanguages.ENGLISH: "en",
    SupportedLanguages.GREEK: "el",
}

# TODO make singleton
class AudioPlayer:
    def __init__(self) -> None:
        try:
            self.os = OperatingSystems(platform.system().lower())
        except KeyError as e:
            raise NotImplementedError from e

    @staticmethod
    def _ahplay_play(audio_file: Path) -> None:
        cmd(f"ahplay {str(audio_file)}")
        # TODO check response

    @staticmethod
    def _vlc_play(audio_file: Path) -> None:
        vlc.MediaPlayer(audio_file).play()  # type: ignore

    def play(self, word: str, language: str) -> None:
        audio_file = Path("temp.mp3")
        tts = gTTS(word, lang=language)
        # TODO put this in temp folder
        tts.save(audio_file)
        if self.os is OperatingSystems.MACOS:
            self._ahplay_play(audio_file)
        elif self.os is OperatingSystems.WINDOWS:
            self._vlc_play(audio_file)
        else:
            raise NotImplementedError


@dataclass
class Flashcard:
    @dataclass
    class Item:
        value: str
        language: InitVar[SupportedLanguages]

        def __post_init__(self, language: SupportedLanguages):
            self._language: str = language_mapping[language]

        @property
        def language(self) -> "str":
            return self._language

    question_text: InitVar[str]
    answer_text: InitVar[str]
    question_language: InitVar[SupportedLanguages]
    answer_language: InitVar[SupportedLanguages]
    keywords: List[str] = field(default_factory=list)

    def __post_init__(
        self,
        question_text: str,
        answer_text: str,
        question_language: SupportedLanguages,
        answer_language: SupportedLanguages,
    ):
        self._player = AudioPlayer()
        self._question = Flashcard.Item(question_text, question_language)
        self._answer = Flashcard.Item(answer_text, answer_language)

    @property
    def question(self) -> str:
        return self._question.value

    @property
    def answer(self) -> str:
        return self._answer.value

    def read_question(self):
        self._player.play(self._question.value, self._question.language)

    def read_answer(self):
        self._player.play(self._answer.value, self._answer.language)

    def show_question(self, console: Console):
        console.print(self._question.value)

    def show_answer(self, console: Console):
        console.print(self._answer.value)
