"""Exceptions."""


class InvalidMoveError(Exception):
    """Raised when move is not allowed."""


class InvalidNotationError(Exception):
    """Raised when chess notation is not valid."""


class OtherPlayersTurnError(Exception):
    """Raised if player moves a white piece on black's turn or vice-versa."""
