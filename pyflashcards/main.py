import csv
import logging
from pathlib import Path
from typing import Any, List, Optional

from pyflashcards.util import setup_logging
from pyflashcards.flashcard import Flashcard, SupportedLanguages
from pyflashcards.flashcard_reader import FlashcardReader

from rich.console import Console

console = Console()
logger = logging.getLogger()


def main():
    setup_logging(Path("main.log"))

    source_file = Path(console.input("Hello! What file should I use to build the flashcards?\n > "))

    # TODO turn this into a generator class
    with open(source_file) as fp:
        csv_reader = csv.reader(fp)
        # Get languages
        question_language, answer_language = next(csv_reader)
        question_language = SupportedLanguages(question_language)
        answer_language = SupportedLanguages(answer_language)

        flashcards: List[Flashcard] = []
        for row in csv_reader:
            question, answer = row
            # keywords = list(keywords.split(",")) TODO
            flashcard = Flashcard(question, answer, question_language, answer_language)
            flashcards.append(flashcard)

        reader = FlashcardReader(console)
        reader.read_flashcards(flashcards)


if __name__ == "__main__":
    main()
