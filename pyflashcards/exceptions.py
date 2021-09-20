"""Exceptions that pertain to Flashcards-level functionality."""


class FlashCardsError(Exception):
    """Base class for other Flashcards-level exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Flashcards Error: {message}")


class InvalidConfiguration(FlashcardsError):
    """Something was attempted that is not possible for the current configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid configuration: {message}")
