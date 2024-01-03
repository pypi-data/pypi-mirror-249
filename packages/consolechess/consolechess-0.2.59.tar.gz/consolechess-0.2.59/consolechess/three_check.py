"""Three-check chess."""

from .board import ChessBoard
from .constants import COLORS
from .datatypes import Color, GameStatus, PieceType, Side
from .utils import other_color


class ThreeCheckBoard(ChessBoard):
    """Three-check chessboard."""

    def __init__(
        self: "ThreeCheckBoard",
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a ThreeCheckBoard."""
        self._checks: dict[Color, int] = {"white": 0, "black": 0}
        super().__init__(fen, pgn, empty=empty, import_fields=import_fields)

    def __repr__(self: "ThreeCheckBoard") -> str:
        """Represent board as string."""
        if self.AUTOPRINT:
            self.print()
        return f"ThreeCheckBoard('{self.fen}')"

    def is_three_check(self: "ThreeCheckBoard") -> bool:
        """Whether a win by three checks has occurred."""
        for color in COLORS:
            if self._checks[color] >= 3:
                self._status = GameStatus(
                    game_over=True,
                    winner=other_color(color),
                    description="three_check",
                )
                return True
        return False

    def move_piece(
        self: "ThreeCheckBoard",
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: bool = False,
    ) -> dict[str, str | bool] | None:
        """Move a game piece."""
        return_val = super().move_piece(
            initial_square,
            final_square,
            allow_castle_and_en_passant=allow_castle_and_en_passant,
            ignore_turn=ignore_turn,
            skip_checks=skip_checks,
            no_disambiguator=no_disambiguator,
            return_metadata=return_metadata,
        )
        if self.king_is_in_check(self.turn):
            self._checks[self.turn] += 1
        if self.is_three_check():
            self._moves[-1] = f"{self._moves[-1].replace('+', '').replace('#', '')}#"
        return return_val

    def en_passant(
        self: "ThreeCheckBoard",
        initial_square: str,
        final_square: str,
        *,
        skip_checks: bool = False,
    ) -> None:
        """Capture an adjacent file pawn that has just made a double forward advance."""
        super().en_passant(initial_square, final_square, skip_checks=skip_checks)
        if self.king_is_in_check(self.turn):
            self._checks[self.turn] += 1
        if self.is_three_check():
            self._moves[-1] = f"{self._moves[-1].replace('+', '').replace('#', '')}#"

    def castle(
        self: "ThreeCheckBoard", color: Color, side: Side, *, skip_checks: bool = False
    ) -> None:
        """
        Move the king two spaces right or left and move the closest rook to its
        other side.
        """
        super().castle(color, side, skip_checks=skip_checks)
        if self.king_is_in_check(self.turn):
            self._checks[self.turn] += 1
        if self.is_three_check():
            self._moves[-1] = f"{self._moves[-1].replace('+', '').replace('#', '')}#"

    def promote_pawn(
        self: "ThreeCheckBoard", square: str, piece_type: PieceType
    ) -> None:
        """Promote a pawn on the farthest rank from where it started."""
        return_val = super().promote_pawn(square, piece_type)
        if self.king_is_in_check(self.turn):
            self._checks[self.turn] += 1
        if self.is_three_check():
            self._moves[-1] = f"{self._moves[-1].replace('+', '').replace('#', '')}#"
        return return_val

    def is_checkmate(self: "ThreeCheckBoard") -> bool:
        """Check if either color's king is checkmated."""
        for color in COLORS:
            if (three_check := self._checks[color] >= 3) or (
                self.king_is_in_check(color)
                and not self.can_block_or_capture_check(color)
                and not self.king_can_escape_check(color)
            ):
                self._status = GameStatus(
                    game_over=True,
                    winner=other_color(color),
                    description="three_check" if three_check else "checkmate",
                )
                return True
        return False
