from __future__ import annotations
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Iterator, Optional, List

from rich.console import Console

from pyflashcards.flashcard import Flashcard


class FlashcardReader:
    class DisplayAction(Enum):
        READ = auto()
        SHOW = auto()

    def __init__(self, console: Console) -> None:
        self._state: Optional[State] = None
        self._console = console
        self.display_action: FlashcardReader.DisplayAction
        self.flashcard: Flashcard
        self._incorrect: List[Flashcard]

    @property
    def state(self) -> State:
        assert self._state is not None
        return self._state

    @state.setter
    def state(self, state: State):
        self._state = state
        self._state._flashcard_reader = self

    def read_flashcards(self, flashcards: List[Flashcard]) -> List[Flashcard]:
        self._incorrect = []
        for flashcard in flashcards:
            self._console.print("\nReading next flashcard...")
            self.read_flashcard(flashcard)
        return self._incorrect

    def read_flashcard(self, flashcard: Flashcard) -> None:
        self.flashcard = flashcard
        self.state = GetDisplayAction()
        while self.state != DoneReadingFlashcard():
            self.state.execute()

    def mark_flashcard_incorrect(self) -> None:
        assert self.flashcard not in self._incorrect
        self._incorrect.append(self.flashcard)


# The common state interface for all the states
class State(ABC):
    def __init__(self) -> None:
        self._flashcard_reader: Optional[FlashcardReader] = None

    def __eq__(self, other: State):
        return self.__class__ == other.__class__

    @property
    def flashcard_reader(self) -> FlashcardReader:
        assert self._flashcard_reader is not None
        return self._flashcard_reader

    @property
    def console(self) -> Console:
        assert self._flashcard_reader is not None
        return self._flashcard_reader._console

    @property
    def flashcard(self) -> Flashcard:
        assert self._flashcard_reader is not None
        return self._flashcard_reader.flashcard

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class GetDisplayAction(State):
    def execute(self) -> None:
        while True:
            user_input = self.console.input(
                "Should I [bold cyan](S)[/bold cyan]how or [bold cyan](R)[/bold cyan]ead the question? "
            ).lower()
            if user_input == "s":
                self.flashcard_reader.display_action = FlashcardReader.DisplayAction.SHOW
                break
            if user_input == "r":
                self.flashcard_reader.display_action = FlashcardReader.DisplayAction.READ
                break
            else:
                self.console.print("Invalid input :sad:")

        self.flashcard_reader.state = DisplayFlashcard()


class DisplayFlashcard(State):
    def execute(self) -> None:
        if self.flashcard_reader.display_action is FlashcardReader.DisplayAction.READ:
            self.flashcard.read_question()
        elif self.flashcard_reader.display_action is FlashcardReader.DisplayAction.SHOW:
            self.flashcard.show_question(self.console)

        self.flashcard_reader.state = WaitForAnswer()


class WaitForAnswer(State):
    def execute(self) -> None:
        while True:
            user_input = self.console.input(
                "[bold cyan](A)[/bold cyan]sk again /[bold cyan](S)[/bold cyan]how the answer? "
            ).lower()
            if user_input == "a":
                self.flashcard_reader.state = DisplayFlashcard()
                break
            elif user_input == "s":
                self.flashcard.show_answer(self.console)
                self.flashcard.read_answer()
                self.flashcard_reader.state = HandleAnswer()
                break
            else:
                self.console.print("Invalid input :sad:")


class HandleAnswer(State):
    def execute(self) -> None:
        while True:
            user_input = self.console.input(
                "[bold cyan](C)[/bold cyan]orrect / [bold cyan](W)[/bold cyan]rong ? "
            ).lower()
            if user_input == "c":
                self.console.print("Well done :smiley:")
                break
            elif user_input == "w":
                self.console.print("I'll store this result so you can try again later.")
                self.flashcard_reader.mark_flashcard_incorrect()
                break
            else:
                self.console.print("Invalid input: sad ")

        self.flashcard_reader.state = DoneReadingFlashcard()


class DoneReadingFlashcard(State):
    def execute(self) -> None:
        pass
