import csv
import logging
from pathlib import Path
from typing import Any, List, Optional

from pyflashcards.util import setup_logging
from pyflashcards.flashcard import Flashcard, SupportedLanguages

from rich.console import Console

console = Console()
logger = logging.getLogger()


def main():
    setup_logging(Path("main.log"))

    source_file = Path(console.input("Hello! What file should I use to build the flashcards?\n > "))

    # TODO turn this into a generator class
    with open(source_file) as fp:
        flashcard_reader = csv.reader(fp)
        # Get languages
        question_language, answer_language = next(flashcard_reader)
        question_language = SupportedLanguages(question_language)
        answer_language = SupportedLanguages(answer_language)

        flashcards: List[Flashcard] = []
        for row in flashcard_reader:
            question, answer = row
            # keywords = list(keywords.split(",")) TODO
            flashcard = Flashcard(question, answer, question_language, answer_language)
            flashcards.append(flashcard)

        incorrect: List[Flashcard] = []

        flashcards_iter = iter(flashcards)
        flashcard = next(flashcards_iter)
        action: Optional[str] = None
        while True:
            # If we don't already know, find out how to display the question
            if not action:
                while not action:
                    action = console.input(
                        "Should I [bold cyan](S)[/bold cyan]how or "
                        "[bold cyan](P)[/bold cyan]lay the question? "
                    ).lower()
                    if action not in ["p", "s"]:
                        action = None
                        console.print("Invalid input :sad:")
                    else:
                        break

            # Now display the question as desired
            if action == "p":
                flashcard.play_question()
            elif action == "s":
                console.print(flashcard.question)

            # Ready for answer?
            try:
                answered = False
                is_done_yet: Optional[str] = None
                while not is_done_yet:
                    is_done_yet = console.input(
                        "[bold cyan](A)[/bold cyan]sk again /[bold cyan](S)[/bold cyan]how the answer? "
                    ).lower()
                    if is_done_yet == "a":
                        is_done_yet = None
                        break
                    elif is_done_yet == "s":
                        action = None
                        answered = True
                        console.print(flashcard.answer)
                        flashcard.play_answer()
                        break
                    else:
                        is_done_yet = None
                        console.print("Invalid input :sad:")

                # Store the result
                done = False
                while answered and not done:
                    user_input = console.input(
                        "[bold cyan](C)[/bold cyan]orrect / [bold cyan](W)[/bold cyan]rong ? "
                    ).lower()
                    if user_input == "c":
                        console.print("Well done :smiley:")
                        console.print("Advancing to the next flashcard...\n")
                        flashcard = next(flashcards_iter)
                        done = True
                    elif user_input == "w":
                        console.print("I'll store this result so you can try again later.\n")
                        flashcard = next(flashcards_iter)
                        incorrect.append(flashcard)
                        done = True
                    else:
                        console.print("Invalid input: sad ")
            except StopIteration:
                console.print("All done!")
                break


if __name__ == "__main__":
    main()
