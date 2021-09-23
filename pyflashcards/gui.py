import csv
from enum import Flag, auto
from pathlib import Path
import logging
from typing import Iterator, Any, List, TypeVar, Generic
from random import randint

import PySimpleGUI as sg

from pyflashcards.flashcard import Flashcard, SupportedLanguages
from pyflashcards.util import setup_logging

logger = logging.getLogger(__name__)

FlashcardCol = sg.Col(
    [
        [
            sg.Text(
                "Waiting to be configured...",
                justification="center",
                expand_x=True,
                expand_y=True,
                font="Any 18",
                auto_size_text=True,
                key="-FLASHCARD-",
            )
        ],
    ],
    size=(500, 300),
    pad=(0, 0),
    expand_x=True,
    expand_y=True,
)

layout = [
    # File browser
    [sg.Text("Where should I read the flashcards from?")],
    [sg.Input(key="-FILEBROWSE-", enable_events=True, expand_x=True), sg.FileBrowse(target="-FILEBROWSE-")],
    # Flashcard
    [
        sg.Frame(
            title="Current Flashcard",
            layout=[[FlashcardCol]],
            relief=sg.RELIEF_RAISED,
            expand_x=True,
            expand_y=True,
        )
    ],
    # Controls
    [
        sg.Checkbox("Read Question Aloud", default=True, enable_events=True, key="-READ-"),
        sg.Checkbox("Print Question to Screen", default=True, enable_events=True, key="-PRINT-"),
    ],
    # Only shown at the end of the test
    [
        sg.Text("1. Select 'Show Answer' when ready to proceed"),
        sg.Button("Repeat Question"),
        sg.Button("Show Answer"),
    ],
    [sg.Text("2. Choose one after seeing the answer:"), sg.Button("Correct"), sg.Button("Wrong")],
    [sg.Button("Retry All", visible=False, key="-RETRY_ALL-")],
    [sg.Button("Retry Only Incorrect", visible=False, key="-RETRY_INCORRECT-")],
]


class DisplayAction(Flag):
    READ = auto()
    SHOW = auto()


T = TypeVar("T")


class ShuffledIterator(Generic[T], Iterator):
    def __init__(self, items: List[T]):
        self._items = items

    def __next__(self) -> T:
        if len(self._items) == 0:
            raise StopIteration
        else:
            return self._items.pop(randint(0, len(self._items) - 1))


class FlashcardsGui:
    def __init__(self) -> None:
        sg.theme("Dark Blue 3")
        self.window = sg.Window("Window Title", layout)
        self.flashcards: ShuffledIterator[Flashcard]
        self.current_flashcard: Flashcard
        self.display_action = DisplayAction.READ | DisplayAction.SHOW
        self.incorrect: List[Flashcard] = []
        self.correct: List[Flashcard] = []

    def set_flashcards(self, flashcards: List[Flashcard]):
        self.flashcards = ShuffledIterator(flashcards)
        self.incorrect = []
        self.correct = []
        self.window.find_element("-RETRY_ALL-").Update(visible=False)
        self.window.find_element("-RETRY_INCORRECT-").Update(visible=False)
        self.get_next_flashcard()

    def get_next_flashcard(self):
        self.current_flashcard = next(self.flashcards)
        self.window["-FLASHCARD-"].update("")
        self.display_current_flashcard()

    def display_current_flashcard(self):
        if DisplayAction.SHOW in self.display_action:
            self.window["-FLASHCARD-"].update(self.current_flashcard.get_question())
        if DisplayAction.READ in self.display_action:
            self.current_flashcard.read_question()

    def run(self):
        try:
            while True:
                # Get the value
                event: Any
                values: Any
                event, values = self.window.read()  # type: ignore
                logger.debug(f"received {event} ==> {values}")

                # Build a new iterator when the input file has changed
                if event == "-FILEBROWSE-":
                    flashcards_file = Path(values["Browse"])
                    logger.info(f"Received new input file: {flashcards_file}")
                    # Build flashcards iterator
                    flashcards: List[Flashcard] = []
                    with open(flashcards_file, encoding="utf-8-sig") as fp:
                        csv_reader = csv.reader(fp)
                        question_language, answer_language = next(csv_reader)
                        question_language = SupportedLanguages(question_language)
                        answer_language = SupportedLanguages(answer_language)
                        for row in csv_reader:
                            question, answer = row
                            # keywords = list(keywords.split(",")) TODO
                            flashcard = Flashcard(question, answer, question_language, answer_language)
                            flashcards.append(flashcard)
                    self.set_flashcards(flashcards)

                # Update the display flag enum
                if event == "-READ-":
                    if values["-READ-"]:
                        logger.info("Enabling flashcards reading")
                        self.display_action |= DisplayAction.READ
                    else:
                        logger.info("Disabling flashcards reading")
                        self.display_action &= ~DisplayAction.READ
                elif event == "-PRINT-":
                    if values["-PRINT-"]:
                        logger.info("Enabling flashcards showing")
                        self.display_action |= DisplayAction.SHOW
                    else:
                        logger.info("Disabling flashcards showing")
                        self.display_action &= ~DisplayAction.SHOW

                # Re-display the flashcard
                if event == "Repeat Question":
                    self.display_current_flashcard()

                # Go to answer
                if event == "Show Answer":
                    self.window["-FLASHCARD-"].update(self.current_flashcard.get_answer())
                    self.current_flashcard.read_answer()

                # Handle the result of the flashcard test
                try:
                    if event == "Correct":
                        logger.info("Marking answer as correct")
                        self.correct.append(self.current_flashcard)
                        self.get_next_flashcard()
                    elif event == "Wrong":
                        logger.info("Marking answer as wrong")
                        self.incorrect.append(self.current_flashcard)
                        self.get_next_flashcard()
                except StopIteration:
                    if len(self.correct) > 0:
                        self.window.find_element("-RETRY_ALL-").Update(visible=True)
                    if len(self.incorrect) > 0:
                        self.window.find_element("-RETRY_INCORRECT-").Update(visible=True)
                    total_questions = len(self.correct) + len(self.incorrect)
                    score = int((len(self.correct) / total_questions) * 100)
                    self.window["-FLASHCARD-"].update(
                        f"That's it. You scored {score}%\n\n"
                        "Choose a Retry button below or select\n a new file to continue"
                    )

                # Handle retries
                if event == "-RETRY_ALL-":
                    logger.info("Retrying all flashcards")
                    self.set_flashcards([*self.correct, *self.incorrect])
                elif event == "-RETRY_INCORRECT-":
                    logger.info("Retrying only incorrect flashcards")
                    self.set_flashcards(self.incorrect)

                # Exit the program
                if event == sg.WIN_CLOSED or event == "Exit":
                    break

        except Exception as e:
            self.window.close()
            raise e


def main():
    global logger
    logger = setup_logging(Path("gui.log"))

    gui = FlashcardsGui()
    gui.run()


if __name__ == "__main__":
    main()
