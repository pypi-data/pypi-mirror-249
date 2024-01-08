"""A chess board."""

from collections import Counter
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from copy import copy
from csv import DictReader
from dataclasses import dataclass
from functools import cache, cached_property, wraps
from pathlib import Path
from platform import system
from random import shuffle
from re import findall, search, sub
from textwrap import TextWrapper
from typing import Any, ClassVar, Final, Literal, TypeVar, overload

from mypy_extensions import mypyc_attr

with suppress(ImportError):
    from rich.console import Console

PieceType = Literal["king", "queen", "rook", "bishop", "knight", "pawn"]
Color = Literal["white", "black"]
Side = Literal["kingside", "queenside"]
StatusDescription = Literal[
    "checkmate",
    "stalemate",
    "opponent_resignation",
    "agreement",
    "threefold_repetition",
    "fivefold_repetition",
    "the_50_move_rule",
    "the_75_move_rule",
    "insufficient_material",
    "imported",
    "explosion",
    "three_check",
    "all_pieces_captured",
]
SquareGenerator = Callable[[str], list[str]]
StepFunction = Callable[[str, int], str | None]

RT = TypeVar("RT")


@dataclass
class Piece:
    """A piece on a chess board."""

    piece_type: PieceType
    color: Color
    promoted: bool = False
    has_moved: bool = False

    def __eq__(self, other: object) -> bool:
        """Check if two pieces are of the same type and color."""
        return (
            (self.piece_type == other.piece_type and self.color == other.color)
            if isinstance(other, Piece)
            else False
        )

    def __hash__(self) -> int:
        """Hash piece (ignores metadata)."""
        if not hasattr(self, "_hash"):
            self._hash = hash((self.piece_type, self.color))
        return self._hash


@dataclass(frozen=True, slots=True)
class GameStatus:
    """Status of the game."""

    game_over: bool
    winner: Color | None = None
    description: StatusDescription | None = None


@dataclass(frozen=True, slots=True)
class Opening:
    """An ECO game opening."""

    eco: str
    name: str
    moves: str


COLORS: Final[tuple[Color, Color]] = ("white", "black")
SIDES: Final[tuple[Side, Side]] = ("queenside", "kingside")
FILES: Final = list("abcdefgh")
SQUARES: Final = [f"{file}{rank}" for rank in range(1, 9) for file in FILES]
PIECE_SYMBOLS: Final[dict[PieceType, str]] = {
    "king": "♚",
    "queen": "♛",
    "rook": "♜",
    "bishop": "♝",
    "knight": "♞",
    "pawn": "♟︎" if "Windows" not in system() else ":chess_pawn:",
}
BLACK_SQUARES: Final = [f"{file}{rank}" for file in "aceg" for rank in (1, 3, 5, 7)] + [
    f"{file}{rank}" for file in "bdfh" for rank in (2, 4, 6, 8)
]
WHITE_SQUARES: Final = [sq for sq in SQUARES if sq not in BLACK_SQUARES]
PLAINTEXT_ABBRS: Final[dict[PieceType, str]] = {
    "knight": "N",
    "rook": "R",
    "bishop": "B",
    "pawn": "P",
    "queen": "Q",
    "king": "K",
}
ALGEBRAIC_PIECE_ABBRS: Final[dict[str, PieceType]] = {
    "K": "king",
    "Q": "queen",
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "": "pawn",
    "P": "pawn",
}
FEN_REPRESENTATIONS: Final = {
    "N": Piece("knight", "white"),
    "K": Piece("king", "white"),
    "R": Piece("rook", "white"),
    "B": Piece("bishop", "white"),
    "Q": Piece("queen", "white"),
    "P": Piece("pawn", "white"),
    "n": Piece("knight", "black"),
    "k": Piece("king", "black"),
    "r": Piece("rook", "black"),
    "b": Piece("bishop", "black"),
    "q": Piece("queen", "black"),
    "p": Piece("pawn", "black"),
}
CASTLING_FINAL_SQUARES: Final[dict[tuple[Color, Side], tuple[str, str]]] = {
    ("white", "kingside"): ("g1", "f1"),  # color, side: rook, king
    ("white", "queenside"): ("c1", "d1"),
    ("black", "kingside"): ("g8", "f8"),
    ("black", "queenside"): ("c8", "d8"),
}
PIECES_TO_TRACK: Final[list[tuple[PieceType, Color, Side | None]]] = [
    ("king", "white", None),
    ("rook", "white", "kingside"),
    ("rook", "white", "queenside"),
    ("king", "black", None),
    ("rook", "black", "kingside"),
    ("rook", "black", "queenside"),
]
WINNER_BY_PGN_RESULT: Final[dict[str, Color | None]] = {
    "1-0": "white",
    "0-1": "black",
    "1/2-1/2": None,
}
PGN_RESULT_BY_WINNER: Final[dict[Color | None, str]] = {
    "white": "1-0",
    "black": "0-1",
    None: "1/2-1/2",
}


class InvalidMoveError(Exception):
    """Raised when move is not allowed."""


class InvalidNotationError(Exception):
    """Raised when chess notation is not valid."""


class OtherPlayersTurnError(Exception):
    """Raised if player moves a white piece on black's turn or vice-versa."""


class GameOverError(Exception):
    """Raised when player attempts to move after game has ended."""


@cache
def other_color(color: Color) -> Color:
    """Get white if black, or black if white."""
    return "black" if color == "white" else "white"


@cache
def get_adjacent_files(square: str) -> list[str]:
    """Get FILES adjacent to square."""
    adjacent_files: list[str] = []
    match square[0]:
        case "a":
            adjacent_files = ["b"]
        case "h":
            adjacent_files = ["g"]
        case _:
            for index in (FILES.index(square[0]) + 1, FILES.index(square[0]) - 1):
                with suppress(IndexError):
                    adjacent_files.append(FILES[index])
    return adjacent_files


@cache
def get_adjacent_squares(square: str) -> list[str]:
    """Get squares to left and right of square."""
    return [f"{file}{square[1]}" for file in get_adjacent_files(square)]


@cache
def iter_to_top(square: str) -> list[str]:
    """Get board squares up to the top (rank 8)."""
    return [f"{square[0]}{rank}" for rank in range(int(square[1]) + 1, 9)]


@cache
def iter_to_bottom(square: str) -> list[str]:
    """Get board squares down to the bottom (rank 1)."""
    return [f"{square[0]}{rank}" for rank in range(int(square[1]) - 1, 0, -1)]


@cache
def iter_to_right(square: str) -> list[str]:
    """Get board squares to the right (file h)."""
    return [f"{file}{square[1]}" for file in FILES[FILES.index(square[0]) + 1 :]]


@cache
def iter_to_left(square: str) -> list[str]:
    """Get board squares to the left (file a)."""
    return [f"{file}{square[1]}" for file in reversed(FILES[: FILES.index(square[0])])]


@cache
def iter_top_right_diagonal(square: str) -> list[str]:
    """Get board squares diagonally upward and to the right from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            FILES[FILES.index(square[0]) + 1 :],
            range(int(square[1]) + 1, 9),
            strict=False,
        )
    ]


@cache
def iter_bottom_left_diagonal(square: str) -> list[str]:
    """Get board squares diagonally downward and to the left from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            reversed(FILES[: FILES.index(square[0])]),
            range(int(square[1]) - 1, 0, -1),
            strict=False,
        )
    ]


@cache
def iter_top_left_diagonal(square: str) -> list[str]:
    """Get board squares diagonally upward and to the left from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            reversed(FILES[: FILES.index(square[0])]),
            range(int(square[1]) + 1, 9),
            strict=False,
        )
    ]


@cache
def iter_bottom_right_diagonal(square: str) -> list[str]:
    """Get board squares diagonally downward and to the right from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            FILES[FILES.index(square[0]) + 1 :],
            range(int(square[1]) - 1, 0, -1),
            strict=False,
        )
    ]


@cache
def step_up(square: str, steps: int) -> str | None:
    """Get square `steps` up from `square`."""
    return (
        f"{square[0]}{rank}"
        if (rank := int(square[1]) + steps) > 0 and rank < 9
        else None
    )


@cache
def step_down(square: str, steps: int) -> str | None:
    """Get square `steps` down from `square`."""
    return (
        f"{square[0]}{rank}"
        if (rank := int(square[1]) - steps) > 0 and rank < 9
        else None
    )


@cache
def step_right(square: str, steps: int) -> str | None:
    """Get square `steps` right from `square`."""
    return (
        f"{FILES[col_index]}{square[1]}"
        if (col_index := FILES.index(square[0]) + steps) >= 0 and col_index <= 7
        else None
    )


@cache
def step_left(square: str, steps: int) -> str | None:
    """Get square `steps` left from `square`."""
    return (
        f"{FILES[col_index]}{square[1]}"
        if (col_index := FILES.index(square[0]) - steps) >= 0 and col_index <= 7
        else None
    )


@cache
def step_diagonal_up_right(square: str, steps: int) -> str | None:
    """Step diagonally to the top and right from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        if cursor is None:
            return None
        cursor = step_right(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_up_left(square: str, steps: int) -> str | None:
    """Step diagonally to the top and left from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        if cursor is None:
            return None
        cursor = step_left(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_down_right(square: str, steps: int) -> str | None:
    """Step diagonally to the bottom and right from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        if cursor is None:
            return None
        cursor = step_right(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_down_left(square: str, steps: int) -> str | None:
    """Step diagonally to the bottom and left from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        if cursor is None:
            return None
        cursor = step_left(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step(square: str, file_offset: int = 0, rank_offset: int = 0) -> str | None:
    """Step multiple directions at once."""
    with suppress(IndexError):
        if (file_idx := FILES.index(square[0]) + file_offset) >= 0 and (
            square := f"{FILES[file_idx]}{int(square[1]) + rank_offset}"
        ) in SQUARES:
            return square
    return None


@cache
def get_squares_between(
    square_1: str, square_2: str, *, strict: bool = False
) -> list[str]:
    """Get the squares between two other squares on the board."""
    if square_1 == square_2:
        return []
    if square_1[0] == square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]):
            iterator = iter_to_top
        else:
            iterator = iter_to_bottom
    elif square_1[0] != square_2[0] and square_1[1] == square_2[1]:
        if FILES.index(square_1[0]) < FILES.index(square_2[0]):
            iterator = iter_to_right
        else:
            iterator = iter_to_left
    elif square_1[0] != square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_top_right_diagonal
        elif int(square_1[1]) < int(square_2[1]):
            iterator = iter_top_left_diagonal
        elif int(square_1[1]) > int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_bottom_right_diagonal
        else:
            iterator = iter_bottom_left_diagonal
    squares_between = []
    met_square_2 = False
    for sq in iterator(square_1):
        if sq == square_2:
            met_square_2 = True
            break
        squares_between.append(sq)
    if met_square_2:
        return squares_between
    else:
        if strict:
            msg = (
                "Squares must be directly diagonal, horizontal,"
                "or vertical to each other."
            )
            raise ValueError(msg)
        else:
            return []


DIRECTION_GENERATORS: Final[dict[tuple[str, str], SquareGenerator]] = {
    ("up", "right"): iter_top_right_diagonal,
    ("up", "inline"): iter_to_top,
    ("up", "left"): iter_top_left_diagonal,
    ("inline", "right"): iter_to_right,
    ("inline", "left"): iter_to_left,
    ("down", "right"): iter_bottom_right_diagonal,
    ("down", "inline"): iter_to_bottom,
    ("down", "left"): iter_bottom_left_diagonal,
}
STEP_FUNCTIONS_BY_DIRECTION: Final[dict[str, StepFunction]] = {
    "up": step_up,
    "right": step_right,
    "left": step_left,
    "down": step_down,
    "up_right": step_diagonal_up_right,
    "up_left": step_diagonal_up_left,
    "down_right": step_diagonal_down_right,
    "down_left": step_diagonal_down_left,
}
ROOK_GENERATORS: Final[list[SquareGenerator]] = [
    iter_to_top,
    iter_to_bottom,
    iter_to_right,
    iter_to_left,
]
BISHOP_GENERATORS: Final[list[SquareGenerator]] = [
    iter_bottom_left_diagonal,
    iter_bottom_right_diagonal,
    iter_top_left_diagonal,
    iter_top_right_diagonal,
]
QUEEN_GENERATORS: Final[list[SquareGenerator]] = ROOK_GENERATORS + BISHOP_GENERATORS
GENERATORS_BY_PIECE_TYPE: Final[dict[PieceType, list[SquareGenerator]]] = {
    "rook": ROOK_GENERATORS,
    "bishop": BISHOP_GENERATORS,
    "queen": QUEEN_GENERATORS,
}
FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR: Final[dict[Color, StepFunction]] = {
    "white": step_up,
    "black": step_down,
}


@cache
def knight_navigable_squares(square: str) -> list[str]:
    """Get knight navigable squares on board."""
    knight_moves = [
        ((dir_1, step_1), (dir_2, step_2))
        for dir_1 in ("up", "down")
        for dir_2 in ("left", "right")
        for step_1, step_2 in ((1, 2), (2, 1))
    ]
    squares = []
    for (dir_1, step_1), (dir_2, step_2) in knight_moves:
        cursor: str | None = square
        assert cursor is not None
        for dir, step in ((dir_1, step_1), (dir_2, step_2)):
            cursor = STEP_FUNCTIONS_BY_DIRECTION[dir](cursor, step)
            if cursor is None:
                break
        if cursor is not None:
            squares.append(cursor)
    return squares


@cache
def king_navigable_squares(square: str) -> list[str]:
    """Get king navigable squares on board."""
    return [
        sq
        for func in STEP_FUNCTIONS_BY_DIRECTION.values()
        if (sq := func(square, 1)) is not None
    ]


@cache
def pawn_capturable_squares(color: Color, square: str) -> list[str]:
    """Get squares a pawn can capture on."""
    pawn_sq_funcs = (
        (step_diagonal_up_left, step_diagonal_up_right)
        if color == "white"
        else (step_diagonal_down_left, step_diagonal_down_right)
    )
    return [sq for func in pawn_sq_funcs if (sq := func(square, 1)) is not None]


@cache
def squares_in_rank(rank: int | str) -> list[str]:
    """Get all squares in rank."""
    return [f"{file}{rank}" for file in FILES]


@cache
def squares_in_file(file: str) -> list[str]:
    """Get all squares in file."""
    return [f"{file}{rank}" for rank in range(1, 9)]


@cache
def en_passant_initial_square(disambiguator: str, color: Color) -> str:
    """Get en passant initial square from disambiguator and moving piece color."""
    return f"{disambiguator}{'5' if color == 'white' else '4'}"


@cache
def en_passant_final_square(double_forward_last_move: str, color: Color) -> str:
    """En passant final square from ChessBoard._double_forward_last_move."""
    final_rank = (
        int(double_forward_last_move[1]) + 1
        if color == "white"
        else int(double_forward_last_move[1]) - 1
    )
    return f"{double_forward_last_move[0]}{final_rank}"


@cache
def en_passant_final_square_from_file(capture_file: str, color: Color) -> str:
    """En passant final square from capture file (i.e. exd6: 'e')."""
    return f"{capture_file}{6 if color == 'white' else 3}"


def read_pgn_database(path: Path | str) -> list[str]:
    """Read a .pgn file to a list of PGN strings."""
    if not isinstance(path, Path):
        path = Path(path)
    with path.open() as file:
        text = file.read()
    pgns = text.split("\n\n[")
    pgns = [f"[{pgn}" for pgn in pgns if len(pgn) > 0 and pgn[0] != "["]
    return pgns


def iter_pgn_database(db: Path | str) -> Iterator[str]:
    """Iterate through PGN strings in file."""
    if not isinstance(db, Path):
        db = Path(db)
    output = ""
    lone_break_ct = 0
    with db.open() as file:
        for line in file:
            output += line
            if line == "\n":
                lone_break_ct += 1
            if lone_break_ct == 2:
                yield output.removesuffix("\n")
                output = ""
                lone_break_ct = 0


def strip_bare_moves_from_pgn(pgn: str, *, strip_numbers: bool = True) -> str:
    """Strip the SAN tokens from a PGN string."""
    pattern = (
        r"\[.+?\]|\{.+?\}|\d+\.+|[10]-[10]|\*|1/2-1/2|[?!]"
        if strip_numbers
        else r"\[.+?\]|\{.+?\}|[10]-[10]|\*|1/2-1/2|[?!]"
    )
    return sub(r"[\n\s]+", " ", sub(pattern, "", pgn)).replace("P@", "@").strip()


def moves_list_from_pgn(pgn: str) -> list[str]:
    """Get list of SAN tokens from a PGN string."""
    return sub(r"\[.+?\]|\{.+?\}|\d+\.+|[10]-[10]|\*|1/2-1/2|[?!]", "", pgn).split()


def get_pgn_field_by_name(pgn: str, name: str) -> str | None:
    """Get PGN field by field name and PGN text."""
    return mat.group(1) if (mat := search(rf"\[{name} \"(.+?)\"\]", pgn)) else None


def pgn_database_to_dicts(path: Path | str) -> list[dict[str, int | str | None]]:
    """Read a .pgn file to a list of dicts."""
    return [
        {
            "game_no": i,
            "variant": get_pgn_field_by_name(pgn, "Variant"),
            "imported_pgn": pgn,
            "imported_bare_moves": strip_bare_moves_from_pgn(pgn),
            "imported_result": get_pgn_field_by_name(pgn, "Result"),
            "imported_termination": get_pgn_field_by_name(pgn, "Termination"),
            "imported_initial_fen": get_pgn_field_by_name(pgn, "FEN"),
        }
        for i, pgn in enumerate(iter_pgn_database(path))
    ]


def block_if_game_over(func: Callable[..., RT]) -> Callable[..., RT]:
    """Raise exception if game is over."""

    @wraps(func)
    def wrapper(self: "ChessBoard", *args: Any, **kwargs: Any) -> Any:
        if self._status.game_over:
            msg = "Game has already ended."
            raise GameOverError(msg)
        return func(self, *args, **kwargs)

    return wrapper


@mypyc_attr(allow_interpreted_subclasses=True)
class ChessBoard:
    """A chess board."""

    AUTOPRINT: ClassVar[bool] = False
    """Print board upon `__repr__` call."""

    ARBITER_DRAW_AFTER_THREEFOLD_REPETITION: ClassVar[bool] = False
    """Do not require claim to draw after threefold repetition."""

    ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK: ClassVar[bool] = False
    """Do not require claim to draw after halfmove clock hits 100 moves."""

    LICHESS_RULES_FOR_INSUFFICIENT_MATERIAL: ClassVar[bool] = False
    """Use Lichess rules for insufficient material. Otherwise, use Chess.com rules."""

    def __init__(
        self,
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a chess board object."""
        self.halfmove_clock = 0
        self.turn: Color = "white"
        self.initial_fen: str | None = None
        self._grid: Final[dict[str, Piece | None]] = {sq: None for sq in SQUARES}
        self._initial_squares: Final[
            dict[tuple[PieceType, Color, Side | None], str]
        ] = {}
        self._has_moved: Final[dict[tuple[PieceType, Color, Side | None], bool]] = {
            piece_tuple: False for piece_tuple in PIECES_TO_TRACK
        }
        self._kings: Final[dict[Color, str]] = {}
        self._double_forward_last_move: str | None = None
        self._status = GameStatus(game_over=False)
        self._moves: list[str] = []
        self._moves_before_fen_import: int = 0
        self._hashes: list[int] = []
        self._must_promote_pawn: str | None = None
        self._fields: Final[dict[str, str]] = {}
        self._move_annotations: dict[str, str] = {}
        if not empty and fen is None and pgn is None:
            self.set_staunton_pattern()
        if fen is not None:
            self.import_fen(fen)
        if pgn is not None:
            return self.import_pgn(pgn, import_fields=import_fields)
        with suppress(StopIteration):
            self.set_initial_positions()

    def __getitem__(self, index: str) -> Piece | None:
        """Get a square's current piece, or None if empty."""
        return self._grid[index]

    def __setitem__(self, index: str, value: Piece | None) -> None:
        """Set a square to a piece or None if setting to empty."""
        if value is not None and value.piece_type == "king":
            self._kings[value.color] = index
        self._grid[index] = value

    def __iter__(self) -> Iterator[str]:
        """Iterate through board."""
        return iter(self._grid)

    def __hash__(self) -> int:
        """Hash position."""
        return hash(
            (
                (black_king_has_moved := self._has_moved["king", "black", None])
                or self._has_moved["rook", "black", "kingside"],
                black_king_has_moved or self._has_moved["rook", "black", "queenside"],
                (white_king_has_moved := self._has_moved["king", "white", None])
                or self._has_moved["rook", "white", "kingside"],
                white_king_has_moved or self._has_moved["rook", "white", "queenside"],
                self._double_forward_last_move if self.can_en_passant() else None,
                self.turn,
                *self._grid.values(),
            )
        )

    def __repr__(self) -> str:
        """Represent ChessBoard as string."""
        if self.AUTOPRINT:
            self.print()
        return f"ChessBoard('{self.fen}')"

    @cached_property
    def opening(self) -> Opening | None:
        """Get the ECO opening."""
        path = (
            Path(f"{Path(__file__).parent}/openings.csv")
            if "__file__" in globals()
            else Path("openings.csv")
        )
        moves = self.export_moves()
        with path.open() as file:
            candidates = [
                opening for opening in DictReader(file) if opening["moves"] in moves
            ]
        longest_len = 0
        if len(candidates) == 0:
            return None
        for candidate in candidates:
            length = len(candidate["moves"])
            if length > longest_len:
                longest = candidate
                longest_len = length
        return Opening(eco=longest["eco"], name=longest["name"], moves=longest["moves"])

    def alternate_turn(self, *, reset_halfmove_clock: bool = False) -> None:
        """Alternate turn, update halfmove clock, and hash position."""
        self.turn = other_color(self.turn)
        self._hashes.append(hash(self))
        self.halfmove_clock = 0 if reset_halfmove_clock else self.halfmove_clock + 1

    def set_staunton_pattern(self) -> None:
        """Add Staunton pattern (initial piece squares)."""
        pairs: tuple[tuple[Color, int, int], ...] = (("white", 1, 2), ("black", 8, 7))
        for color, pc_rank, pawn_rank in pairs:
            for file in FILES:
                self[f"{file}{pawn_rank}"] = Piece("pawn", color)
            self[f"a{pc_rank}"] = Piece("rook", color)
            self[f"b{pc_rank}"] = Piece("knight", color)
            self[f"c{pc_rank}"] = Piece("bishop", color)
            self[f"d{pc_rank}"] = Piece("queen", color)
            self[f"e{pc_rank}"] = Piece("king", color)
            self[f"f{pc_rank}"] = Piece("bishop", color)
            self[f"g{pc_rank}"] = Piece("knight", color)
            self[f"h{pc_rank}"] = Piece("rook", color)

    @contextmanager
    def test_position(self, changes: dict[str, Piece | None]) -> Iterator[None]:
        """
        Make temporary changes to the board to test properties of a position.
        Do not raise exceptions within a `test_position` context manager.
        """
        original_contents = {sq: self._grid[sq] for sq in changes}
        for sq in changes:
            self[sq] = changes[sq]
        yield
        for sq in original_contents:
            self[sq] = original_contents[sq]

    def set_random(self) -> None:
        """Set board for Fischer random chess / Chess960."""
        ranks_and_colors: list[tuple[int, Color]] = [(2, "white"), (7, "black")]
        for rank, color in ranks_and_colors:
            for sq in squares_in_rank(rank):
                self[sq] = Piece("pawn", color)
        major_pieces = [
            "knight",
            "knight",
            "bishop_1",
            "bishop_2",
            "rook_1",
            "rook_2",
            "queen",
            "king",
        ]
        while True:
            shuffle(major_pieces)
            # Check if bishops are on opposite-color squares.
            bishop_1 = f"a{major_pieces.index('bishop_1')}"
            bishop_2 = f"a{major_pieces.index('bishop_2')}"
            if (bishop_1 in BLACK_SQUARES) == (bishop_2 in BLACK_SQUARES):
                continue
            # Check if king is in between rooks.
            rook_1_rank = major_pieces.index("rook_1")
            rook_2_rank = major_pieces.index("rook_2")
            a_side_rook = rook_1_rank if rook_1_rank < rook_2_rank else rook_2_rank
            h_side_rook = rook_1_rank if a_side_rook == rook_2_rank else rook_1_rank
            king_rank = major_pieces.index("king")
            if king_rank > h_side_rook or king_rank < a_side_rook:
                continue
            break
        # Populate board.
        major_rank_and_colors: list[tuple[int, Color]] = [(1, "white"), (8, "black")]
        for rank, color in major_rank_and_colors:
            for i, piece in enumerate(major_pieces):
                pt: PieceType = piece.removesuffix("_1").removesuffix("_2")  # type: ignore
                self[f"{FILES[i]}{rank}"] = Piece(pt, color)
        self.set_initial_positions()
        self.initial_fen = self.fen
        self._fields["Variant"] = "Chess960"

    def set_initial_positions(self) -> None:
        """Set initial positions of pieces used for castling."""
        for color in COLORS:
            rooks = [
                sq
                for sq in SQUARES
                if (pc := self._grid[sq]) is not None
                and pc.piece_type == "rook"
                and pc.color == color
            ]
            match len(rooks):
                case 2:
                    self._initial_squares["rook", color, "queenside"] = (
                        rooks[0]
                        if FILES.index(rooks[0][0]) < FILES.index(rooks[1][0])
                        else rooks[1]
                    )
                    self._initial_squares["rook", color, "kingside"] = (
                        rooks[0]
                        if self._initial_squares["rook", color, "queenside"] != rooks[0]
                        else rooks[1]
                    )
                case 1:
                    for side in SIDES:
                        self._initial_squares["rook", color, side] = rooks[0]
            if self._kings.get(color) is None:
                with suppress(StopIteration):
                    self._kings[color] = next(
                        sq
                        for sq in SQUARES
                        if (pc := self._grid[sq]) is not None
                        and pc.piece_type == "king"
                        and pc.color == color
                    )
            with suppress(KeyError):
                self._initial_squares["king", color, None] = self._kings[color]

    def import_pgn(self, pgn: str, *, import_fields: bool = True) -> None:
        """Import a game by PGN string."""
        pgn = pgn.replace("\n", " ")
        if "[FEN " in pgn and (match := search(r"\[FEN \"(.+?)\"\]", pgn)):
            fen = match.group(1)
            self.import_fen(fen)
        else:
            self.set_staunton_pattern()
        self.set_initial_positions()
        self.submit_moves(pgn)
        if import_fields:
            self._fields.update(dict(findall(r"\[([^\s]+) \"(.+?)\"\]", pgn)))
            self._move_annotations = dict(findall(r"(\d+\.+)[^\.\{]+?\{(.+?)\}", pgn))
        if (
            import_fields
            and not self.status.game_over
            and (result := search(r"\[Result \"(.+?)\"\]", pgn))
        ):
            match result.group(1):
                case "1/2-1/2":
                    self.draw()
                case "1-0" | "0-1" as res:
                    self._status = GameStatus(
                        game_over=True,
                        winner=WINNER_BY_PGN_RESULT[res],
                        description="imported",
                    )

    def import_fen(self, fen: str) -> None:
        """Import Forsyth-Edwards Notation to board."""
        if match := search(
            r"(?P<R8>[^/]+)/(?P<R7>[^/]+)/(?P<R6>[^/]+)/(?P<R5>[^/]+)/"
            r"(?P<R4>[^/]+)/(?P<R3>[^/]+)/(?P<R2>[^/]+)/(?P<R1>[^/\s]+) "
            r"(?P<turn>[wb]) (?P<castling>[KQkqA-Ha-h-]+) (?P<enpassant>[a-h1-8-]+)"
            r"(?: (?P<halfmove>\d+) (?P<fullmove>\d+))?",
            fen,
        ):
            groups = match.groups()
        else:
            msg = "Could not read FEN."
            raise ValueError(msg)

        # Populate board.
        for rank, group in zip(range(8, 0, -1), groups[:8], strict=True):
            cursor = f"a{rank}"
            for char in group:
                if char.isalpha():
                    self[cursor] = copy(FEN_REPRESENTATIONS[char])
                    if (cur := step_right(cursor, 1)) is not None:
                        cursor = cur
                elif char.isnumeric():
                    self[cursor] = None
                    if (cur := step_right(cursor, int(char))) is not None:
                        cursor = cur

        # Set turn.
        self.turn = "white" if groups[8] == "w" else "black"

        # Set en passant target square.
        if groups[10] != "-":
            self._double_forward_last_move = (
                f"{groups[10][0]}{5 if groups[10][1] == 6 else 4}"
            )

        # Set halfmove clock.
        if groups[11] is not None:
            self.halfmove_clock = int(groups[11])

        # Set fullmove number.
        if groups[12] is not None:
            self._moves_before_fen_import = int(groups[12]) - 1
            if groups[8] == "b":
                self._moves.append("_")

        # Set initial position variables for rooks and kings.
        self.set_initial_positions()

        # Set castling availability.
        if groups[9] == "-":
            for color in COLORS:
                self._has_moved["king", color, None] = True
                self[self._kings[color]]
        else:
            for color in COLORS:
                chars_defined = False
                with suppress(KeyError):
                    queenside_rook_char = (
                        sq[0]
                        if (sq := self._initial_squares["rook", color, "queenside"])
                        is not None
                        else "q"
                    )
                    kingside_rook_char = (
                        sq[0]
                        if (sq := self._initial_squares["rook", color, "kingside"])
                        is not None
                        else "k"
                    )
                    chars_defined = True
                if chars_defined:
                    if (
                        "K" not in groups[9]
                        and kingside_rook_char.upper() not in groups[9]
                    ):
                        self._has_moved["rook", "white", "kingside"] = True
                    if (
                        "Q" not in groups[9]
                        and queenside_rook_char.upper() not in groups[9]
                    ):
                        self._has_moved["rook", "white", "queenside"] = True
                    if "k" not in groups[9] and kingside_rook_char not in groups[9]:
                        self._has_moved["rook", "black", "kingside"] = True
                    if "q" not in groups[9] and queenside_rook_char not in groups[9]:
                        self._has_moved["rook", "black", "queenside"] = True
                    break

        self.initial_fen = fen

    @property
    def fen(self) -> str:
        """Export the board in Forsyth-Edwards Notation."""
        return self.export_fen()

    def export_fen(self, *, no_clocks: bool = False, shredder: bool = False) -> str:
        """Export the board in Forsyth-Edwards Notation."""
        fen = ""
        # Concatenate piece placement data.
        for rank in range(8, 0, -1):
            blank_sq_counter = 0
            for sq in squares_in_rank(rank):
                if (piece := self._grid[sq]) is None:
                    blank_sq_counter += 1
                    continue
                if blank_sq_counter > 0:
                    fen += str(blank_sq_counter)
                    blank_sq_counter = 0
                char = PLAINTEXT_ABBRS[piece.piece_type]
                fen += char.upper() if piece.color == "white" else char.lower()
            if blank_sq_counter > 0:
                fen += str(blank_sq_counter)
            if rank > 1:
                fen += "/"
        # Concatenate active color.
        fen += f" {self.turn[0]} "
        # Concatenate castling availability.
        castling_symbols: dict[tuple[Color, Side], str] = {
            ("white", "kingside"): "K",
            ("black", "kingside"): "k",
            ("white", "queenside"): "Q",
            ("black", "queenside"): "q",
        }
        if shredder:
            for color, side in castling_symbols:
                castling_symbols[color, side] = (
                    self._initial_squares["rook", color, side][0].upper()
                    if color == "white"
                    else self._initial_squares["rook", color, side][0]
                )
        any_castles_possible = False
        for color in COLORS:
            for side in SIDES:
                if (
                    not self._has_moved["king", color, None]
                    and not self._has_moved["rook", color, side]
                ):
                    fen += castling_symbols[color, side]
                    any_castles_possible = True
        if not any_castles_possible:
            fen += "-"
        fen += " "
        # Concatenate en passant target square.
        if self._double_forward_last_move is not None:
            fen += self._double_forward_last_move[0]
            if self._double_forward_last_move[1] == "4":
                fen += "3"
            if self._double_forward_last_move[1] == "5":
                fen += "6"
        else:
            fen += "-"
        # Concatenate halfmove and fullmove clocks.
        if not no_clocks:
            fen += f" {self.halfmove_clock} {self.fullmove_clock}"

        return fen

    @property
    def fullmove_clock(self) -> int:
        """Return the current move number, as it appears in FEN notation."""
        return self._moves_before_fen_import + (len(self._moves) // 2) + 1

    @property
    def pgn(self) -> str:
        """Export game in Portable Game Notation."""
        return self.export_pgn()

    def export_pgn(
        self,
        fields: dict[str, str] | None = None,
        *,
        wrap: int | None = 80,
        include_current_position: bool = False,
        include_opening: bool = True,
    ) -> str:
        """Export game in Portable Game Notation."""
        fields_ = self._fields if fields is None else fields
        output = ""
        header_fields = ["Event", "Site", "Date", "Round", "White", "Black"]
        for field in header_fields:
            if field in fields_:
                output += f'[{field} "{self._fields[field]}"]\n'
        if not self._status.game_over:
            output += '[Result "*"]\n'
        else:
            output += f'[Result "{PGN_RESULT_BY_WINNER[self._status.winner]}"]\n'
        if self.initial_fen is not None:
            if "SetUp" not in fields_:
                output += '[SetUp "1"]\n'
            if "FEN" not in fields_:
                output += f'[FEN "{self.initial_fen}"]\n'
        if include_opening and (opening := self.opening) is not None:
            if "ECO" not in self._fields:
                output += f'[ECO "{opening.eco}"]\n'
            if "Opening" not in self._fields:
                output += f'[Opening "{opening.name}"]\n'
        for name, value in self._fields.items():
            if name not in header_fields and name != "Result":
                output += f'[{name} "{value}"]\n'
        if include_current_position:
            output += f'[CurrentPosition "{self.fen}"]\n'
        output += f"\n{self.export_moves(include_annotations=True, wrap=wrap)}\n"
        return output

    @property
    def epd(self) -> str:
        """Return Extended Position Description (EPD) as string."""
        return self.export_epd()

    def export_epd(
        self,
        fields: dict[str, str] | None = None,
        *,
        include_hmvc: bool = False,
        include_fmvn: bool = False,
    ) -> str:
        """Return Extended Position Description (EPD) as string."""
        output = self.export_fen(no_clocks=True)
        if include_hmvc:
            output += f" hvmc {self.halfmove_clock};"
        if include_fmvn:
            output += f" fmvn {self.fullmove_clock};"
        if fields is not None:
            for field in fields:
                output += f" {field} {fields[field]};"
        return output

    def _pseudolegal_squares(
        self,
        initial_square: str,
        *,
        capture_only: bool = False,
        check_castle: bool = True,
    ) -> Iterator[str]:
        """
        Get all pseudolegal squares for a given piece.
        This includes squares occupied by the king or which, if moved to,
        would put the king in check. Use ChessBoard.legal_moves()
        to only include legal moves.

        If capture_only is True, only include squares which are eligible for capture.
        In other words, pawn forward moves will not be included in return list.

        If check_castle is True, yield post-castling positions for kings.
        """
        if (piece := self._grid[initial_square]) is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        match piece.piece_type:
            case "pawn":
                return self._pawn_pseudolegal_squares(
                    initial_square, piece, capture_only=capture_only
                )
            case "rook" | "queen" | "bishop":
                return self._queen_rook_bishop_pseudolegal_squares(
                    initial_square, piece
                )
            case "knight":
                return self._knight_pseudolegal_squares(initial_square, piece)
            case "king":
                return self._king_pseudolegal_squares(
                    initial_square, piece, check_castle=check_castle
                )

    def legal_moves(self, square: str) -> Iterator[str]:
        """Get legal moves for a piece."""
        if (piece := self._grid[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        for sq in self._pseudolegal_squares(square):
            # If the piece is a pawn diagonal to the pseudolegal square,
            # and the square at pseudolegal square is None, it must be an en passant.
            if (
                piece.piece_type == "pawn"
                and sq[0] in get_adjacent_files(square)
                and self._grid[sq] is None
            ):
                if self.can_en_passant(square, sq[0]):
                    yield sq
            # If the piece is a king, it could be a castle.
            elif piece.piece_type == "king" and (
                (sq in ("c1", "g1", "c8", "g8") and self.can_castle(piece.color))
                or self.can_move_piece(square, sq, navigability_already_checked=True)
            ):
                yield sq
            # Otherwise, it goes through move_piece.
            else:
                if self.can_move_piece(square, sq, navigability_already_checked=True):
                    yield sq

    def can_move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        navigability_already_checked: bool = False,
    ) -> bool:
        """
        Check if a piece can be moved to final_square without castling or en passant.
        Does not check turn.
        """
        piece = self._grid[initial_square]
        piece_at_final_square = self._grid[final_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        if (
            not navigability_already_checked
            and final_square
            not in self._pseudolegal_squares(initial_square, check_castle=False)
        ):
            return False
        if (
            piece_at_final_square is not None
            and piece_at_final_square.piece_type == "king"
            and piece_at_final_square.color == piece.color
        ):
            return False
        with self.test_position({final_square: piece, initial_square: None}):
            if self.king_is_in_check(piece.color):
                return False
        return True

    def _pawn_pseudolegal_squares(
        self,
        initial_square: str,
        piece: Piece,
        *,
        capture_only: bool = False,
    ) -> Iterator[str]:
        """Get pawn's pseudolegal squares (ignores king capture rules)."""
        step_func = FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR[piece.color]
        # forward and double forward advance
        if (
            not capture_only
            and (sq := step_func(initial_square, 1)) is not None
            and self._grid[sq] is None
        ):
            yield sq
            if (
                initial_square[1] == ("2" if piece.color == "white" else "7")
                and (sq := step_func(initial_square, 2)) is not None
                and self._grid[sq] is None
            ):
                yield sq
        # diagonal capture
        yield from (
            sq
            for sq in pawn_capturable_squares(piece.color, initial_square)
            if (pc := self._grid[sq]) is not None and pc.color != piece.color
        )
        # en passant capture
        if self._double_forward_last_move in get_adjacent_squares(initial_square):
            yield en_passant_final_square(self._double_forward_last_move, piece.color)

    def _queen_rook_bishop_pseudolegal_squares(
        self, initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get queen's pseudolegal squares (ignores king capture rules)."""
        for generator in GENERATORS_BY_PIECE_TYPE[piece.piece_type]:
            for sq in generator(initial_square):
                if (other_piece := self._grid[sq]) is None:
                    yield sq
                else:
                    if other_piece.color != piece.color:
                        yield sq
                    break

    def _knight_pseudolegal_squares(
        self, initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get knight pseudolegal squares (ignores king capture rules)."""
        return (
            sq
            for sq in knight_navigable_squares(initial_square)
            if (pc := self._grid[sq]) is None or pc.color != piece.color
        )

    def _king_pseudolegal_squares(
        self,
        initial_square: str,
        piece: Piece,
        *,
        check_castle: bool = False,
    ) -> Iterator[str]:
        """Get king pseudolegal squares (ignores king capture rules)."""
        yield from (
            sq
            for sq in king_navigable_squares(initial_square)
            if (pc := self._grid[sq]) is None or pc.color != piece.color
        )
        if check_castle:
            yield from (
                CASTLING_FINAL_SQUARES[piece.color, side][1]
                for side in SIDES
                if self.can_castle(piece.color, side)
            )

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: Literal[False],
    ) -> None: ...

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: Literal[True],
    ) -> dict[str, str | bool]: ...

    @overload
    def move_piece(
        self,
        initial_square: str,
        final_square: str,
        *,
        allow_castle_and_en_passant: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: bool = False,
    ) -> dict[str, str | bool] | None: ...

    @block_if_game_over
    def move_piece(
        self,
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
        piece = self._grid[initial_square]
        if not skip_checks and self._must_promote_pawn is not None:
            if piece is None:
                msg = f"No piece at initial_square '{initial_square}'."
                raise InvalidMoveError(msg)
            msg = (
                f"Must promote pawn at square '{self._must_promote_pawn}' "
                "before next move."
            )
            raise InvalidMoveError(msg)
        assert piece is not None
        if allow_castle_and_en_passant:
            # Try to castle if king is moving to a final castling square,
            # or if rook is jumping over a king.
            castle_side: Side = "queenside" if final_square[0] in "cd" else "kingside"
            if (
                piece.piece_type == "king"
                and final_square in ("c1", "c8", "g1", "g8")
                and self.can_castle(piece.color, castle_side)
            ):
                self.castle(piece.color, castle_side, skip_checks=True)
                return (
                    {"move_type": "castle", "side": castle_side}
                    if return_metadata
                    else None
                )
            # Reroute to self.en_passant if pawn captures on empty final square.
            if (
                piece.piece_type == "pawn"
                and initial_square[0] != final_square[0]
                and self._grid[final_square] is None
            ):
                self.en_passant(initial_square, final_square)
                return (
                    {"move_type": "en_passant", "capture": True}
                    if return_metadata
                    else None
                )

        if not skip_checks:
            # Check correct player's piece is being moved.
            if not ignore_turn and piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            # Check piece can navigate to square.
            if final_square not in self._pseudolegal_squares(
                initial_square, check_castle=False
            ):
                msg = "Not a valid move."
                raise InvalidMoveError(msg)
            # Test if king would be in check if moved.
            king_would_be_in_check = False
            with self.test_position({final_square: piece, initial_square: None}):
                if self.king_is_in_check(self.turn):
                    king_would_be_in_check = True
            if king_would_be_in_check:
                msg = "Cannot move piece because king would be in check."
                raise InvalidMoveError(msg)

        # Add piece type notation, disambiguating if necessary.
        piece_at_final_square = self._grid[final_square]
        notation = (
            PLAINTEXT_ABBRS[piece.piece_type] if piece.piece_type != "pawn" else ""
        )
        notation += self._write_disambiguator(
            initial_square,
            final_square,
            piece,
            piece_at_final_square,
            no_disambiguator=no_disambiguator,
        )

        # Update clocks and notation to denote capture, and raise exceptions
        # for illegal captures.
        if piece_at_final_square is not None:
            if piece.piece_type == "pawn" and len(notation) == 0:
                notation += initial_square[0]
            notation += "x"
            is_capture = True
            if piece_at_final_square.color == piece.color:
                msg = "Cannot place piece at square occupied by same color piece."
                raise InvalidMoveError(msg)
            elif piece_at_final_square.piece_type == "king":
                msg = "Cannot capture king."
                raise InvalidMoveError(msg)
        else:
            is_capture = False
        notation += final_square

        # Update has_moved variables (used to determine castling availability).
        if piece.piece_type == "king":
            self._has_moved["king", piece.color, None] = True
        elif piece.piece_type == "rook":
            if initial_square == self._initial_squares.get(
                ("rook", piece.color, "kingside")
            ):
                side: Side | None = "kingside"
            elif initial_square == self._initial_squares.get(
                ("rook", piece.color, "queenside")
            ):
                side = "queenside"
            else:
                side = None
            if side is not None:
                self._has_moved["rook", piece.color, side] = True
        self._double_forward_last_move = (
            final_square
            if piece.piece_type == "pawn"
            and abs(int(initial_square[1]) - int(final_square[1])) == 2
            else None
        )

        # Move piece.
        self[initial_square] = None
        if not piece.has_moved and piece.piece_type == "pawn":
            piece = Piece(
                piece_type=piece.piece_type,
                color=piece.color,
                promoted=piece.promoted,
                has_moved=True,
            )
        self[final_square] = piece

        # If pawn moving to final rank, require pawn promotion. Else, check
        # for check / checkmate, append moves, and return.
        if piece.piece_type == "pawn" and final_square[1] in ("1", "8"):
            self._must_promote_pawn = final_square
        else:
            self._must_promote_pawn = None
            if self.king_is_in_check(oc := other_color(self.turn)):
                if self.is_checkmate(kings_known_in_check=[oc]):
                    notation += "#"
                else:
                    notation += "+"
            self.alternate_turn(
                reset_halfmove_clock=(piece.piece_type == "pawn" or is_capture),
            )
        self._moves.append(notation)
        return (
            (
                {
                    "move_type": "normal",
                    "capture": is_capture,
                    "capture_piece_type": piece_at_final_square.piece_type,
                    "capture_piece_is_promoted": piece_at_final_square.promoted,
                }
                if piece_at_final_square is not None
                else {"move_type": "normal", "capture": is_capture}
            )
            if return_metadata
            else None
        )

    def _write_disambiguator(
        self,
        initial_square: str,
        final_square: str,
        piece: Piece,
        piece_at_final_square: Piece | None,
        *,
        no_disambiguator: bool = False,
    ) -> str:
        if no_disambiguator:
            return ""
        disambiguator = ""
        match piece.piece_type:
            case "rook" | "bishop" | "queen" as pt:
                ambiguous_pieces: list[str] = []
                generators: list[SquareGenerator] = GENERATORS_BY_PIECE_TYPE[pt]
                for generator in generators:
                    for sq in generator(final_square):
                        if (pc := self._grid[sq]) == piece:
                            if sq != initial_square and self.can_move_piece(
                                sq, final_square
                            ):
                                ambiguous_pieces.append(sq)
                            break
                        elif pc is not None:
                            break
            case "pawn":
                # Forward moves are unambiguous by nature.
                if piece_at_final_square is None:
                    ambiguous_pieces = []
                # If the piece is not None, it must be a diagonal capture.
                else:
                    ambiguous_pieces = []
                    step_funcs = (
                        (step_diagonal_up_left, step_diagonal_up_right)
                        if piece_at_final_square.color == "white"
                        else (step_diagonal_down_left, step_diagonal_down_right)
                    )
                    for func in step_funcs:
                        if (
                            (square := func(final_square, 1)) is not None
                            and square != initial_square
                            and self._grid[square] is not None
                            and self.can_move_piece(square, final_square)
                        ):
                            ambiguous_pieces = [square]
            case "knight":
                ambiguous_pieces = [
                    sq
                    for sq in knight_navigable_squares(final_square)
                    if self._grid[sq] == piece
                    and sq != initial_square
                    and self.can_move_piece(sq, final_square)
                ]
            case "king":
                ambiguous_pieces = []
        if len(ambiguous_pieces) > 0:
            possible_disambiguators = (
                initial_square[0],
                initial_square[1],
                initial_square,
            )
            for possible_disambiguator in possible_disambiguators:
                still_ambiguous_pieces = [
                    sq
                    for sq in ambiguous_pieces
                    if possible_disambiguator in sq and sq != initial_square
                ]
                if len(still_ambiguous_pieces) == 0:
                    disambiguator = possible_disambiguator
                    break
        return disambiguator

    def submit_moves(self, *notations: str) -> None:
        """Submit multiple moves at once with algebraic notation."""
        if len(notations) == 1 and " " in notations[0]:
            notations = tuple(moves_list_from_pgn(notations[0]))
            if len(notations) == 1 and notations[0] == "":
                return None
        for notation in notations:
            self.move(notation)

    @property
    def moves(self) -> str:
        """Export moves to string."""
        return self.export_moves()

    def export_moves(
        self,
        *,
        include_annotations: bool = False,
        wrap: int | None = None,
    ) -> str:
        """Export moves to string."""
        i = self._moves_before_fen_import
        output = ""
        moves = self._moves
        while True:
            i += 1
            if len(moves) == 1:
                move_no = f"{i}."
                move_annotation = f"{move_no} {moves[0]}"
                output += move_annotation
                if include_annotations and move_no in self._move_annotations:
                    output += f" {{{self._move_annotations[move_no]}}} "
            if len(moves) < 2:
                break
            move_no = f"{i}."
            output += f"{move_no} {moves[0]} "
            if include_annotations and move_no in self._move_annotations:
                output += f"{{{self._move_annotations[move_no]}}} {i}... "
            output += f"{moves[1]} "
            if include_annotations and (no := f"{i}...") in self._move_annotations:
                output += f"{{{self._move_annotations[no]}}} "
            moves = moves[2:]
        st = self.status
        output += f" {PGN_RESULT_BY_WINNER[st.winner]}" if st.game_over else " *"
        output = sub(r"\. _", "...", output).strip().replace("  ", " ")
        return "\n".join(TextWrapper(width=wrap).wrap(output)) if wrap else output

    @overload
    def move(
        self, notation: str, *, return_metadata: Literal[False] = False
    ) -> None: ...

    @overload
    def move(
        self, notation: str, *, return_metadata: Literal[True]
    ) -> dict[str, str | bool]: ...

    @block_if_game_over
    def move(
        self, notation: str, *, return_metadata: bool = False
    ) -> dict[str, str | bool] | None:
        """Make a move using algebraic notation."""
        if "O-O" in notation:
            side: Side = "queenside" if "O-O-O" in notation else "kingside"
            self.castle(self.turn, side)
            return (
                {"move_type": "castle", "side": side, "capture": False}
                if return_metadata
                else None
            )
        elif match := search(
            r"([KQRBN]?)([a-h1-8]{,2})x?([a-h][1-8])[\(=/]?([KQRBN]?)\)?\s?.*$",
            notation,
        ):
            piece_type = ALGEBRAIC_PIECE_ABBRS[match.group(1)]
            disambiguator = match.group(2)
            final_square = match.group(3)
            pawn_promotion = (
                ALGEBRAIC_PIECE_ABBRS[grp] if (grp := match.group(4)) != "" else None
            )
            initial_square = self._read_disambiguator(
                notation, piece_type, disambiguator, final_square
            )
            if "x" in notation and self._grid[final_square] is None:
                with suppress(InvalidMoveError):
                    self.en_passant(initial_square, final_square)
                    return (
                        {
                            "move_type": "en_passant",
                            "capture": True,
                            "capture_piece_type": "pawn",
                            "capture_piece_is_promoted": False,
                        }
                        if return_metadata
                        else None
                    )
            if (
                piece_type == "pawn"
                and final_square[1] in ("1", "8")
                and pawn_promotion is None
            ):
                msg = "Must promote pawn upon move to final rank."
                raise InvalidMoveError(msg)
            return_val = self.move_piece(
                initial_square,
                final_square,
                allow_castle_and_en_passant=False,
                no_disambiguator=(disambiguator == ""),
                return_metadata=return_metadata,
            )
            if pawn_promotion is not None:
                self.promote_pawn(final_square, pawn_promotion)
                if return_val is not None:
                    return_val["promote_pawn"] = True
            return return_val
        else:
            msg = f"Could not read notation '{notation}'."
            raise InvalidNotationError(msg)

    def _read_disambiguator(
        self,
        notation: str,
        piece_type: PieceType,
        disambiguator: str,
        final_square: str,
    ) -> str:
        match piece_type:
            case "rook" | "bishop" | "queen" as pt:
                candidates = []
                for generator in GENERATORS_BY_PIECE_TYPE[pt]:
                    for sq in generator(final_square):
                        piece = self._grid[sq]
                        if (
                            disambiguator in sq
                            and piece is not None
                            and piece.piece_type == piece_type
                            and piece.color == self.turn
                        ):
                            candidates.append(sq)
                        elif piece is not None:
                            break
            case "pawn":
                candidates = []
                # If capturing but moving to an empty square, it must be an
                # en passant. For en passant moves, the file must also be
                # specified (e.g. "exf6"). We know the initial rank by
                # color, so there is only one candidate.
                if "x" in notation and self._grid[final_square] is None:
                    candidates = [en_passant_initial_square(disambiguator, self.turn)]
                # If no piece at final square, it must be a forward advance.
                elif self._grid[final_square] is None:
                    step_func = FORWARD_STEP_FUNCTIONS_BY_PAWN_COLOR[
                        other_color(self.turn)
                    ]
                    if (
                        (square := step_func(final_square, 1)) is not None
                        and disambiguator in square
                        and (pc := self._grid[square]) is not None
                        and pc.piece_type == "pawn"
                        and pc.color == self.turn
                    ) or (
                        (square := step_func(final_square, 2)) is not None
                        and disambiguator in square
                        and (pc := self._grid[square]) is not None
                        and pc.piece_type == "pawn"
                        and pc.color == self.turn
                    ):
                        candidates.append(square)
                # Otherwise, it's a capture.
                else:
                    for square in pawn_capturable_squares(
                        other_color(self.turn), final_square
                    ):
                        if (
                            square is not None
                            and disambiguator in square
                            and (pc := self._grid[square]) is not None
                            and pc.piece_type == "pawn"
                            and pc.color == self.turn
                        ):
                            candidates.append(square)
            case "knight":
                candidates = [
                    sq
                    for sq in knight_navigable_squares(final_square)
                    if disambiguator in sq
                    and (pc := self._grid[sq]) is not None
                    and pc.piece_type == "knight"
                    and pc.color == self.turn
                ]
            case "king":
                candidates = (
                    [king_sq] if (king_sq := self._kings[self.turn]) is not None else []
                )
        if len(candidates) == 1:
            initial_square = candidates[0]
        elif len(candidates) == 0:
            msg = f"'{notation}' is not allowed."
            raise InvalidNotationError(msg)
        else:
            successful_candidates = [
                candidate
                for candidate in candidates
                if self.can_move_piece(candidate, final_square)
            ]
            if len(successful_candidates) == 1:
                initial_square = successful_candidates[0]
            elif len(candidates) == 0:
                msg = f"'{notation}' is not allowed."
                raise InvalidNotationError(msg)
            else:
                msg = f"Must disambiguate moving pieces: {successful_candidates}"
                raise InvalidNotationError(msg)
        return initial_square

    def can_castle(self, color: Color, side: Side | None = None) -> bool:
        """Check if a player can castle. Optionally specify side."""
        king_has_moved = self._has_moved["king", color, None]
        if (
            king_has_moved
            or (king_sq := self._initial_squares.get(("king", color, None))) is None
        ):
            return False
        allowed_pcs = (None, Piece("rook", color), Piece("king", color))
        return any(
            rook_init_sq is not None
            and not rook_has_moved
            and (pc := self._grid[rook_init_sq]) is not None
            and pc.piece_type == "rook"
            and pc.color == color
            and all(
                self._grid[sq] is None
                for sq in get_squares_between(king_sq, rook_init_sq)
            )
            and all(self._grid[sq] in allowed_pcs for sq in final_squares)
            and not self.king_is_in_check(color)
            and not any(
                sq in get_squares_between(king_sq, final_squares[0])
                for sq in self.checked_squares(color)
            )
            for rook_init_sq, rook_has_moved, final_squares in [
                (
                    self._initial_squares.get(("rook", color, side_)),
                    self._has_moved["rook", color, side_],
                    CASTLING_FINAL_SQUARES[color, side_],
                )
                for side_ in ([side] if side is not None else SIDES)
            ]
        )

    @block_if_game_over
    def castle(
        self,
        color: Color,
        side: Side,
        *,
        skip_checks: bool = False,
    ) -> None:
        """
        Move the king two spaces right or left and move the closest rook
        to its other side.
        """
        if not skip_checks:
            if color != self.turn:
                msg = f"It is {self.turn.upper()}'s turn."
                raise OtherPlayersTurnError(msg)
            if self._must_promote_pawn is not None:
                msg = (
                    f"Must promote pawn at square '{self._must_promote_pawn}' "
                    "before next move."
                )
                raise InvalidMoveError(msg)
        if skip_checks or self.can_castle(color, side):
            king_final_sq, rook_final_sq = CASTLING_FINAL_SQUARES[color, side]
            rook_init_sq = self._initial_squares["rook", color, side]
            assert rook_init_sq is not None
            self[self._kings[color]] = None
            self._grid[rook_init_sq] = None
            self[king_final_sq] = Piece("king", color)
            self._grid[rook_final_sq] = Piece("rook", color)
            self._has_moved["king", color, None] = True
            self._has_moved["rook", color, side] = True
            self._double_forward_last_move = None
            notation = "O-O" if side == "kingside" else "O-O-O"
            if self.king_is_in_check(oc := other_color(self.turn)):
                if self.is_checkmate(kings_known_in_check=[oc]):
                    notation += "#"
                else:
                    notation += "+"
            self._moves.append(notation)
            self._must_promote_pawn = None
            self.alternate_turn()
        else:
            msg = "Castling not allowed."
            raise InvalidMoveError(msg)

    def promote_pawn(self, square: str, piece_type: PieceType) -> None:
        """Promote a pawn on the farthest rank from where it started."""
        if (piece := self._grid[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        if piece.color != self.turn:
            msg = f"It is {self.turn}'s turn."
            raise OtherPlayersTurnError(msg)
        if (piece.color == "white" and square[1] != "8") or (
            piece.color == "black" and square[1] != "1"
        ):
            msg = (
                "Cannot promote pawn unless it is at farthest rank from where it "
                "started."
            )
            raise InvalidMoveError(msg)
        self._grid[square] = Piece(
            piece_type, piece.color, promoted=True, has_moved=True
        )
        self._double_forward_last_move = None
        self._must_promote_pawn = None
        updated_notation = f"{self._moves[-1]}={PLAINTEXT_ABBRS[piece_type]}"
        if self.king_is_in_check(oc := other_color(self.turn)):
            if self.is_checkmate(kings_known_in_check=[oc]):
                updated_notation += "#"
            else:
                updated_notation += "+"
        self._moves[-1] = updated_notation
        self.alternate_turn(reset_halfmove_clock=True)

    def can_en_passant(
        self,
        initial_square: str | None = None,
        capture_file: str | None = None,
    ) -> bool:
        """Check if an en passant capture is possible."""
        if self._double_forward_last_move is None:
            return False
        if initial_square is None:
            return any(
                (pc := self._grid[sq]) is not None
                and pc.piece_type == "pawn"
                and pc.color == self.turn
                for sq in get_adjacent_squares(self._double_forward_last_move)
            )
        candidate_squares = []
        for func in (step_left, step_right):
            if (square := func(initial_square, 1)) is None:
                continue
            if capture_file is None or capture_file in square:
                candidate_squares.append(square)
        if (
            self._double_forward_last_move not in candidate_squares
            or (piece := self._grid[initial_square]) is None
        ):
            return False
        color = piece.color
        with self.test_position(
            {
                initial_square: None,
                en_passant_final_square_from_file(capture_file, color): Piece(
                    "pawn", color
                ),
                self._double_forward_last_move: None,
            }
        ):
            if self.king_is_in_check(color):
                return False
        return True

    @block_if_game_over
    def en_passant(
        self,
        initial_square: str,
        final_square: str,
        *,
        skip_checks: bool = False,
    ) -> None:
        """Capture an adjacent file pawn that has just made a double forward advance."""
        piece = self[initial_square]
        if not skip_checks:
            if piece is None:
                msg = f"No piece at initial_square '{initial_square}'."
                raise InvalidMoveError(msg)
            if piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            if self._must_promote_pawn is not None:
                msg = (
                    f"Must promote pawn at square '{self._must_promote_pawn}' "
                    "before next move."
                )
                raise InvalidMoveError(msg)
        assert piece is not None
        if skip_checks or self.can_en_passant(initial_square, final_square[0]):
            assert self._double_forward_last_move is not None
            self._grid[self._double_forward_last_move] = None
            self._grid[initial_square] = None
            self._grid[final_square] = piece
            self._double_forward_last_move = None
            notation = f"{initial_square[0]}x{final_square}"
            if self.king_is_in_check(oc := other_color(self.turn)):
                if self.is_checkmate(kings_known_in_check=[oc]):
                    notation += "#"
                else:
                    notation += "+"
            self._moves.append(notation)
            self._must_promote_pawn = None
            self.alternate_turn(reset_halfmove_clock=True)

    @property
    def pieces(self) -> dict[str, Piece]:
        """Get all pieces on the board."""
        return {sq: piece for sq in self._grid if (piece := self._grid[sq]) is not None}

    def checked_squares(self, color: Color) -> Iterator[str]:
        """Get all checked squares for a color."""
        oc = other_color(color)
        other_color_pieces = [
            sq for sq in self if (pc := self._grid[sq]) is not None and pc.color == oc
        ]
        already_yielded: list[str] = []
        for init_sq in other_color_pieces:
            for sq in self._pseudolegal_squares(
                init_sq, capture_only=True, check_castle=False
            ):
                if sq not in already_yielded:
                    yield sq
                    already_yielded.append(sq)

    def is_checkmate(self, *, kings_known_in_check: list[Color] | None = None) -> bool:
        """Check if either color's king is checkmated."""
        for color in COLORS:
            if (
                (
                    (kings_known_in_check is not None and color in kings_known_in_check)
                    or self.king_is_in_check(color)
                )
                and not self.can_block_or_capture_check(color)
                and not self.king_can_escape_check(color)
            ):
                self._status = GameStatus(
                    game_over=True, winner=other_color(color), description="checkmate"
                )
                return True
        return False

    def is_stalemate(self, pieces: dict[str, Piece] | None = None) -> bool:
        """Check if the game is a stalemate."""
        pieces_ = self.pieces if pieces is None else pieces
        if all(
            list(self.legal_moves(sq)) == []
            for sq in pieces_
            if pieces_[sq].color == self.turn
        ) and not self.can_castle(self.turn):
            self._status = GameStatus(game_over=True, description="stalemate")
            return True
        return False

    def is_draw_by_fivefold_repetition(self) -> bool:
        """Check if any position has repeated 5 times or more."""
        with suppress(IndexError):
            if Counter(self._hashes).most_common(1)[0][1] >= 5:
                self._status = GameStatus(
                    game_over=True, description="fivefold_repetition"
                )
                return True
        return False

    def is_draw_by_insufficient_material(
        self, pieces: dict[str, Piece] | None = None
    ) -> bool:
        """Check if board has insufficient material."""
        pieces_ = self.pieces if pieces is None else pieces
        white_pieces = []
        black_pieces = []
        for sq in pieces_:
            if (pc := pieces_[sq]).color == "white":
                white_pieces.append(pc.piece_type)
            else:
                black_pieces.append(pc.piece_type)
        pieces_by_color = white_pieces, black_pieces
        if not self.LICHESS_RULES_FOR_INSUFFICIENT_MATERIAL:
            for pcs, other_pcs in pieces_by_color, pieces_by_color[::-1]:
                counter = Counter(pcs)
                if (
                    counter["pawn"] > 0
                    or counter["rook"] > 0
                    or counter["queen"] > 0
                    or counter["bishop"] > 1
                    or (counter["bishop"] > 0 and counter["knight"] > 0)
                    or (counter["knight"] > 1 and other_pcs != ["king"])
                ):
                    return False
            self._status = GameStatus(
                game_over=True, description="insufficient_material"
            )
            return True
        else:
            is_sufficient = False
            for color_pieces, other_color_pieces in (
                pieces_by_color,
                pieces_by_color[::-1],
            ):
                if any(pt in color_pieces for pt in ("rook", "pawn", "queen")):
                    is_sufficient = True
                    break
                if color_pieces.count("knight") + color_pieces.count("bishop") > 1:
                    is_sufficient = True
                    break
                if "knight" in color_pieces and any(
                    pt in other_color_pieces
                    for pt in ("rook", "knight", "bishop", "pawn")
                ):
                    is_sufficient = True
                    break
                if "bishop" in color_pieces and (
                    "knight" in other_color_pieces or "pawn" in other_color_pieces
                ):
                    is_sufficient = True
                    break
                if "bishop" in color_pieces and "bishop" in color_pieces:
                    bishops = [
                        sq for sq in pieces_ if pieces_[sq].piece_type == "bishop"
                    ]
                    bishop_square_colors = {
                        ("white" if bishop in WHITE_SQUARES else "black")
                        for bishop in bishops
                    }
                    if len(bishop_square_colors) == 2:
                        is_sufficient = True
                        break
            if not is_sufficient:
                self._status = GameStatus(
                    game_over=True, description="insufficient_material"
                )
                return True
            return False

    def is_draw_by_75_move_rule(self) -> bool:
        """Check if draw by 75 moves without pawn move or capture."""
        if self.halfmove_clock >= 150:
            self._status = GameStatus(game_over=True, description="the_75_move_rule")
            return True
        return False

    @property
    def status(self) -> GameStatus:
        """Check the board for a checkmate or draw."""
        pieces = self.pieces
        if (
            self._status.game_over
            or self.is_checkmate()
            or self.is_stalemate(pieces)
            or (
                self.ARBITER_DRAW_AFTER_THREEFOLD_REPETITION
                and self.can_claim_draw_by_threefold_repetition()
            )
            or self.is_draw_by_fivefold_repetition()
            or self.is_draw_by_insufficient_material(pieces)
            or (
                self.ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK
                and self.can_claim_draw_by_halfmove_clock()
            )
            or self.is_draw_by_75_move_rule()
        ):
            return self._status
        return GameStatus(game_over=False)

    def can_block_or_capture_check(
        self, color: Color, *, drop_pool: list[PieceType] | None = None
    ) -> bool | None:
        """
        Return True if a check can be blocked by another piece or if the threatening
        piece can be captured.
        """
        pieces = self.pieces
        same_color_pieces_except_king = []
        other_color_pieces = []
        king: str | None = None
        for sq in pieces:
            if (pc := pieces[sq]).color == color:
                if pc.piece_type == "king":
                    king = sq
                else:
                    same_color_pieces_except_king.append(sq)
            else:
                other_color_pieces.append(sq)
        if king is None:
            return None
        squares_that_would_block_check = []
        for check in (
            checks := [
                piece
                for piece in other_color_pieces
                if king
                in self._pseudolegal_squares(
                    piece, capture_only=True, check_castle=False
                )
            ]
        ):
            if (rank_difference := int(king[1]) - int(check[1])) > 0:
                rank_direction = "up"  # i.e. king is upward of piece
            else:
                rank_direction = "inline" if rank_difference == 0 else "down"
            if (file_difference := FILES.index(king[0]) - FILES.index(check[0])) > 0:
                file_direction = "right"  # i.e. king is to the right of piece
            else:
                file_direction = "inline" if file_difference == 0 else "left"
            possible_squares = [
                check,
                *list(DIRECTION_GENERATORS[rank_direction, file_direction](check)),
            ]
            if (pt := pieces[check].piece_type) in ("knight", "pawn"):
                squares_that_would_block_check.append(check)
            if pt in ("rook", "bishop", "queen"):
                for square in possible_squares:
                    if square == king:
                        break
                    squares_that_would_block_check.append(square)
        # In variants like Crazyhouse, a piece can be dropped on the board
        # to block checkmate.
        if drop_pool is not None and drop_pool != [] and len(checks) == 1:
            no_drop_on_first_or_eighth = set(drop_pool) == {"pawn"}
            for sq in squares_that_would_block_check:
                if sq not in checks and not (
                    no_drop_on_first_or_eighth and sq[1] in ("1", "8")
                ):
                    return True
        possible_moves: list[tuple[str, str]] = []  # [(from, to), ...]
        for sq in same_color_pieces_except_king:
            possible_moves.extend(
                [
                    (sq, move)
                    for move in self._pseudolegal_squares(sq, check_castle=False)
                ]
            )
        # Check if en passant capture can block check.
        if self._double_forward_last_move is not None:
            for square in get_adjacent_squares(self._double_forward_last_move):
                if (
                    (piece := self._grid[square]) is not None
                    and piece.piece_type == "pawn"
                    and piece.color == color
                    and self.can_en_passant(square, self._double_forward_last_move[0])
                ):
                    with self.test_position(
                        {
                            self._double_forward_last_move: None,
                            square: None,
                            en_passant_final_square(
                                self._double_forward_last_move, color
                            ): Piece("pawn", color),
                        }
                    ):
                        if not self.king_is_in_check(color):
                            return True
        squares_that_can_be_moved_to = [move[1] for move in possible_moves]
        for square in squares_that_can_be_moved_to:
            if square in squares_that_would_block_check:
                candidates = [move for move in possible_moves if move[1] == square]
                for initial_sq, final_sq in candidates:
                    with self.test_position(
                        {initial_sq: None, final_sq: self._grid[initial_sq]}
                    ):
                        if not self.king_is_in_check(color):
                            return True
        return False

    def _is_check_by_rook_bishop_queen(self, color: Color, king_sq: str) -> bool:
        for generator_list, types in (
            (ROOK_GENERATORS, ("rook", "queen")),
            (BISHOP_GENERATORS, ("bishop", "queen")),
        ):
            for generator in generator_list:
                for sq in generator(king_sq):
                    if (
                        (pc := self._grid[sq]) is not None
                        and pc.color != color
                        and pc.piece_type in types
                    ):
                        return True
                    elif pc is not None:
                        break
        return False

    def _is_check_by_pawn(self, color: Color, king_sq: str) -> bool:
        return any(
            (pc := self._grid[sq]) is not None
            and pc.piece_type == "pawn"
            and pc.color == other_color(color)
            for sq in pawn_capturable_squares(color, king_sq)
        )

    def _is_check_by_knight_king(self, color: Color, king_sq: str) -> bool:
        return any(
            (pc := self._grid[sq]) is not None
            and pc.piece_type == pt
            and pc.color == other_color(color)
            for func, pt in (
                (king_navigable_squares, "king"),
                (knight_navigable_squares, "knight"),
            )
            for sq in func(king_sq)
        )

    def king_is_in_check(self, color: Color) -> bool | None:
        """Whether king is in check."""
        if (king_sq := self._kings.get(color)) is None:
            return None
        if (
            self._is_check_by_rook_bishop_queen(color, king_sq)
            or self._is_check_by_pawn(color, king_sq)
            or self._is_check_by_knight_king(color, king_sq)
        ):
            return True
        return False

    def king_can_escape_check(self, color: Color) -> bool | None:
        """Whether a king can escape check (assuming it is in check)."""
        return (
            len(list(self.legal_moves(king))) > 0
            if self._grid[king := self._kings[color]] is not None
            else None
        )

    def resign(self, color: Color | None = None) -> GameStatus:
        """Resign instead of moving."""
        self._status = GameStatus(
            game_over=True,
            winner=other_color(self.turn) if color is None else other_color(color),
            description="opponent_resignation",
        )
        return self._status

    def draw(self) -> GameStatus:
        """Draw instead of moving."""
        if self.can_claim_draw():
            return self.claim_draw()
        self._status = GameStatus(game_over=True, description="agreement")
        return self._status

    def can_claim_draw(self) -> bool:
        """Whether draw can be claimed without agreement."""
        return (
            self.can_claim_draw_by_halfmove_clock()
            or self.can_claim_draw_by_threefold_repetition()
        )

    def can_claim_draw_by_halfmove_clock(self) -> bool:
        """Whether draw can be claimed due to 50 moves without pawn move or capture."""
        can_claim = self.halfmove_clock >= 100
        if can_claim and self.ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK:
            self._status = GameStatus(game_over=True, description="the_50_move_rule")
        return can_claim

    def can_claim_draw_by_threefold_repetition(self) -> bool:
        """Whether draw can be claimed due to threefold repetition."""
        try:
            can_claim = Counter(self._hashes).most_common(1)[0][1] >= 3
            if can_claim and self.ARBITER_DRAW_AFTER_THREEFOLD_REPETITION:
                self._status = GameStatus(
                    game_over=True, description="threefold_repetition"
                )
        except IndexError:
            return False
        else:
            return can_claim

    def claim_draw(self) -> GameStatus:
        """Claim a draw due to 50 moves without a capture or pawn move."""
        if self._status.game_over:
            return self._status
        if (move_rule := self.halfmove_clock >= 100) or (
            Counter(self._hashes).most_common(1)[0][1] >= 3
        ):
            self._status = GameStatus(
                game_over=True,
                description="the_50_move_rule" if move_rule else "threefold_repetition",
            )
            return self._status
        return GameStatus(game_over=False)

    @property
    def _rich_renderable(self) -> str:
        """Get a Rich renderable representation of the board."""
        losing_king_sq: str | None = None
        winning_king_sq: str | None = None
        if self.status.description == "checkmate":
            with suppress(KeyError):
                assert self._status.winner is not None
                losing_king_sq = self._kings[other_color(self._status.winner)]
        if self._status.winner is not None:
            with suppress(KeyError):
                winning_king_sq = self._kings[self._status.winner]
        rank_renderable = "\n"
        for rank in range(8, 0, -1):
            rank_renderable += f"[white]{rank}[/white] "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self._grid[sq]
                if piece is not None:
                    symbol = "#" if sq == losing_king_sq else " "
                    if sq == winning_king_sq:
                        color_tags = ("[reverse][#FFD700]", "[/reverse][/#FFD700]")
                    else:
                        color_tags = (
                            ("[reverse][#ffffff]", "[/#ffffff][/reverse]")
                            if piece.color == "white"
                            else ("[white]", "[/white]")
                        )
                    rank_renderable += (
                        f"{color_tags[0]}{PIECE_SYMBOLS[piece.piece_type]}"
                        f"{symbol}{color_tags[1]}"
                    )
                else:
                    rank_renderable += (
                        "[reverse][#789656]  [/reverse][/#789656]"
                        if sq in BLACK_SQUARES
                        else "[reverse][#f0edd1]  [/reverse][/#f0edd1]"
                    )
            rank_renderable += "\n"
        rank_renderable += "[bold][white]  a b c d e f g h [/bold][/white]\n"
        return rank_renderable

    @property
    def ascii(self) -> str:
        """Get an ASCII representation of the board."""
        winning_king_sq = None
        if self.status.description == "checkmate":
            winning_king_sq = self._kings[self._status.winner]  # type: ignore
        output = ""
        for rank in range(8, 0, -1):
            output += f"{rank} "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self._grid[sq]
                if piece is None:
                    output += ". "
                else:
                    output += (
                        f"{PLAINTEXT_ABBRS[piece.piece_type].upper()}"
                        f"{'#' if sq == winning_king_sq else ' '}"
                        if piece.color == "white"
                        else f"{PLAINTEXT_ABBRS[piece.piece_type].lower()} "
                    )
            output += "\n"
        output += "  a b c d e f g h "
        return output

    def print(self, *, plaintext: bool = False) -> None:
        """Print the ChessBoard to console."""
        if not plaintext and "Console" in globals():
            Console().print(self._rich_renderable)
        else:
            print(self.ascii)
