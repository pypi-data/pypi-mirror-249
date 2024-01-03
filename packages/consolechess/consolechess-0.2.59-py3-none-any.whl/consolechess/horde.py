"""Horde variant of chess."""

from collections.abc import Iterator

from .board import ChessBoard
from .datatypes import GameStatus, Piece
from .utils import FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR


class HordeBoard(ChessBoard):
    """A chess board to play Horde."""

    def __init__(
        self: "HordeBoard",
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a HordeBoard."""
        super().__init__(fen=fen, pgn=pgn, empty=True, import_fields=import_fields)
        if not empty:
            self.import_fen(
                "rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP "
                "w qk - 0 1"
            )
        self._fields["Variant"] = "Horde"

    def __repr__(self: "HordeBoard") -> str:
        """Represent board as string."""
        if self.AUTOPRINT:
            self.print()
        return f"HordeBoard('{self.fen}')"

    def _pawn_pseudolegal_squares(
        self: "HordeBoard",
        initial_square: str,
        piece: Piece,
        *,
        capture_only: bool = False,
    ) -> Iterator[str]:
        yield from super()._pawn_pseudolegal_squares(
            initial_square, piece, capture_only=capture_only
        )
        if not capture_only and piece.has_moved:
            step_func = FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR[piece.color]
            if (
                (sq := step_func(initial_square, 1)) is not None
                and self._grid[sq] is None
                and (sq := step_func(initial_square, 2)) is not None
                and self._grid[sq] is None
            ):
                yield sq

    def is_checkmate(self: "ChessBoard") -> bool:
        """Check if either color's king is checkmated."""
        pieces = self.pieces
        if all(pieces[pc].color == "black" for pc in pieces):
            self._status = GameStatus(
                game_over=True, winner="black", description="checkmate"
            )
            return True
        # NOTE: Replace with super().is_checkmate?
        if (
            self.king_is_in_check("black")
            and not self.can_block_or_capture_check("black")
            and not self.king_can_escape_check("black")
        ):
            self._status = GameStatus(
                game_over=True,
                winner="white",
                description="checkmate",
            )
            return True
        return False
