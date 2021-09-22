import csv
from enum import Flag, auto
from pathlib import Path
import logging
from typing import Iterator, Any, List

import PySimpleGUI as sg

from pyflashcards.flashcard import Flashcard, SupportedLanguages, AudioPlayer
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
    [sg.Input(key="-FILEBROWSE-", enable_events=True), sg.FileBrowse(target="-FILEBROWSE-")],
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
        sg.Checkbox("Read aloud", default=True, enable_events=True, key="-READ-"),
        sg.Checkbox("Print question", default=True, enable_events=True, key="-PRINT-"),
    ],
    [sg.Button("Repeat"), sg.Button("Correct"), sg.Button("Wrong")],
    [sg.Button("Exit")],
]


class DisplayAction(Flag):
    READ = auto()
    SHOW = auto()


class FlashcardsGui:
    def __init__(self) -> None:
        sg.theme("Dark Blue 3")
        self.window = sg.Window("Window Title", layout)
        self.flashcards: Iterator[Flashcard]
        self.current_flashcard: Flashcard
        self.display_action = DisplayAction.READ | DisplayAction.SHOW
        self.incorrect: List[Flashcard] = []

    def get_next_flashcard(self):
        # TODO handle end of iterator
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
                    flashcards_list: List[Flashcard] = []
                    with open(flashcards_file) as fp:
                        csv_reader = csv.reader(fp)
                        question_language, answer_language = next(csv_reader)
                        question_language = SupportedLanguages(question_language)
                        answer_language = SupportedLanguages(answer_language)
                        for row in csv_reader:
                            question, answer = row
                            # keywords = list(keywords.split(",")) TODO
                            flashcard = Flashcard(question, answer, question_language, answer_language)
                            flashcards_list.append(flashcard)
                    self.flashcards = iter(flashcards_list)
                    self.get_next_flashcard()
                    self.incorrect = []

                # Update the display flag enum
                if event == "-READ-":
                    if values["-READ-"]:
                        logger.info("Enabling flashcards reading")
                        self.display_action |= DisplayAction.READ
                    else:
                        logger.info("Disabling flashcards reading")
                        self.display_action &= ~DisplayAction.READ
                if event == "-PRINT-":
                    if values["-PRINT-"]:
                        logger.info("Enabling flashcards showing")
                        self.display_action |= DisplayAction.SHOW
                    else:
                        logger.info("Disabling flashcards showing")
                        self.display_action &= ~DisplayAction.SHOW

                # Re-display the flashcard
                if event == "Repeat":
                    self.display_current_flashcard()

                # Handle the result of the flashcard test
                if event == "Correct":
                    self.get_next_flashcard()
                if event == "Wrong":
                    self.get_next_flashcard()

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
