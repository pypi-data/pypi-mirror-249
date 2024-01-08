"""Crazyhouse chess."""

import re
from typing import Literal, overload

from .board import (
    ALGEBRAIC_PIECE_ABBRS,
    PLAINTEXT_ABBRS,
    ChessBoard,
    Color,
    InvalidMoveError,
    InvalidNotationError,
    Piece,
    PieceType,
    other_color,
)


class CrazyhouseBoard(ChessBoard):
    """A game of Crazyhouse chess."""

    def __init__(
        self,
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

    def __repr__(self) -> str:
        """Represent board as string."""
        if self.AUTOPRINT:
            self.print()
        return f"CrazyhouseBoard('{self.fen}')"

    def can_drop_piece(
        self,
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
        self,
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
        if self.king_is_in_check(oc := other_color(self.turn)):
            if self.is_checkmate(kings_known_in_check=[oc]):
                notation += "#"
            else:
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
        self, notation: str, *, return_metadata: bool = False
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
        self,
        color: Color,
        *,
        drop_pool: list[PieceType] | None = None,
    ) -> bool | None:
        """Return True if a check can be blocked by another piece."""
        return super().can_block_or_capture_check(
            color, drop_pool=self._pools[color] if drop_pool is None else drop_pool
        )
