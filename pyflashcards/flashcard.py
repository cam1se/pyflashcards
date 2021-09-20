import enum
import platform
from dataclasses import InitVar, dataclass, field
from typing import List
import logging

from gtts import gTTS

from pyflashcards.util import cmd

logger = logging.getLogger(__name__)

# TODO get this from gTTS
class SupportedLanguages(enum.Enum):
    ENGLISH = "english"
    GREEK = "greek"


language_mapping = {
    SupportedLanguages.ENGLISH: "en",
    SupportedLanguages.GREEK: "el",
}


# TODO make singleton
class AudioPlayer:
    def __init__(self) -> None:
        os = None
        if (p := platform.system().lower()) == "darwin":
            self.player = "afplay"
            os = "MacOS"
        else:
            raise NotImplementedError

        assert os is not None
        logger.debug(f"Using {self.player} to play audio on {os}")

    def play(self, word: str, language: str) -> None:
        tts = gTTS(word, lang=language)
        # TODO put this in temp folder
        tts.save("temp.mp3")
        response = cmd(f"{self.player} temp.mp3")


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

    def play_question(self):
        self._player.play(self._question.value, self._question.language)

    def play_answer(self):
        self._player.play(self._answer.value, self._answer.language)
