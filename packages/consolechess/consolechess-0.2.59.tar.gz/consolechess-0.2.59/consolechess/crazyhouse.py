"""
Crazyhouse chess.

From https://www.chess.com/article/view/crazyhouse-chess on 12/22/2023:

    "Rules: The standard rules of chess apply to crazyhouse with these additions.
    - When you capture an opponent's piece, it is placed in your "pool" of pieces and
    you can "drop" it on an empty square on your turn.
    - Pieces may only be dropped on empty squares.
    - You may drop a piece to give check or checkmate.
    - Pawns may not be dropped on the first or eighth ranks.

    Notation: In order to record drops in crazyhouse the @ symbol is used. An example
    would be N@g3 which means a 'knight is dropped from the pool to the square g3.'"

From https://en.wikipedia.org/wiki/Crazyhouse on 12/22/2023:
    "When a piece that is promoted from a pawn is captured, it enters the opponent's
    reserve as a pawn."

"""

import re
from typing import Literal, overload

from .board import ChessBoard
from .constants import ALGEBRAIC_PIECE_ABBRS, COLORS, PLAINTEXT_ABBRS
from .datatypes import Color, GameStatus, Piece, PieceType
from .exceptions import InvalidMoveError, InvalidNotationError
from .utils import other_color


class CrazyhouseBoard(ChessBoard):
    """A game of Crazyhouse chess."""

    def __init__(
        self: "CrazyhouseBoard",
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a Crazyhouse board."""
        self._pools: dict[Color, list[PieceType]] = {"white": [], "black": []}
        super().__init__(fen=fen, pgn=pgn, empty=empty, import_fields=import_fields)
        self._fields["Variant"] = "Crazyhouse"

    def __repr__(self: "CrazyhouseBoard") -> str:
        """Represent board as string."""
        if self.AUTOPRINT:
            self.print()
        return f"CrazyhouseBoard('{self.fen}')"

    def _hash_grid(self: "CrazyhouseBoard") -> int:
        return hash(
            (
                *self._pools["white"],
                None,
                *self._pools["black"],
                None,
                *self._grid.items(),
            )
        )

    def can_drop_piece(
        self: "CrazyhouseBoard",
        square: str,
        piece: Piece,
        *,
        ignore_turn: bool = False,
    ) -> bool:
        """Check if a piece can be dropped to a certain square."""
        with self.test_position({square: piece}):
            if self.king_is_in_check(piece.color):
                return False
        return (
            piece.piece_type in self._pools[piece.color]
            and self._grid[square] is None
            and not (piece.piece_type == "pawn" and square[1] in ("1", "8"))
            and (ignore_turn or self.turn == piece.color)
        )

    def drop_piece(
        self: "CrazyhouseBoard",
        square: str,
        piece: Piece,
        *,
        skip_checks: bool = False,
    ) -> None:
        """Drop a piece from a player's pool onto the board."""
        if not (skip_checks or self.can_drop_piece(square, piece)):
            return None
        self[square] = piece
        abbr = PLAINTEXT_ABBRS[piece.piece_type] if piece.piece_type != "pawn" else ""
        notation = f"{abbr}@{square}"
        self.alternate_turn()
        hash_ = self._hash_grid()
        if self.is_checkmate(hash_):
            notation += "#"
        elif self.king_is_in_check(other_color(piece.color)):
            notation += "+"
        self._moves.append(notation)
        self._pools[piece.color].remove(piece.piece_type)

    @overload
    def move(
        self: "ChessBoard", notation: str, *, return_metadata: Literal[False] = False
    ) -> None: ...

    @overload
    def move(
        self: "ChessBoard", notation: str, *, return_metadata: Literal[True]
    ) -> dict[str, str | bool]: ...

    def move(
        self: "CrazyhouseBoard", notation: str, *, return_metadata: bool = False
    ) -> dict[str, str | bool] | None:
        """Make a move using algebraic notation."""
        if "@" in notation:
            if match := re.search(r"(.?)@([a-h][1-8])", notation):
                piece_type = ALGEBRAIC_PIECE_ABBRS[match.group(1)]
                square = match.group(2)
                if self.can_drop_piece(square, (pc := Piece(piece_type, self.turn))):
                    self.drop_piece(square, pc)
                    return {"move_type": "drop"} if return_metadata else None
                else:
                    msg = "Cannot drop piece."
                    raise InvalidMoveError(msg)
            else:
                msg = f"Could not read move notation '{notation}'."
                raise InvalidNotationError(msg)
        move_output = super().move(notation, return_metadata=True)
        if (
            move_output is not None
            and "capture" in move_output
            and move_output["capture"]
        ):
            self._pools[other_color(self.turn)].append(
                "pawn"
                if move_output["capture_piece_is_promoted"]
                else move_output["capture_piece_type"]  # type: ignore
            )
        return move_output if return_metadata else None

    def can_block_or_capture_check(
        self: "CrazyhouseBoard",
        color: Color,
        *,
        drop_pool: list[PieceType] | None = None,
    ) -> bool | None:
        """Return True if a check can be blocked by another piece."""
        return super().can_block_or_capture_check(
            color, drop_pool=self._pools[color] if drop_pool is None else drop_pool
        )

    def is_checkmate(self: "CrazyhouseBoard", hash: int | None = None) -> bool:
        """Check if either color's king is checkmated."""
        for color in COLORS:
            if (
                self.king_is_in_check(color)
                and not self.can_block_or_capture_check(color)
                and not self.king_can_escape_check(color)
            ):
                self._status = GameStatus(
                    game_over=True,
                    winner=other_color(color),
                    description="checkmate",
                )
                return True
        return False
