"""Chess in the Terminal, but a little bit fancier."""

import re
from pathlib import Path
from sys import argv
from typing import ClassVar

import pyperclip  # type: ignore
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Click
from textual.widgets import Button, Footer, Header, Input, Static

from .board import BLACK_SQUARES, FILES, PIECE_SYMBOLS, ChessBoard, Piece

last_tile_clicked: str | None = None


class Tile(Static):
    """A chess board tile."""

    def on_click(self: "Tile") -> None:
        """Handle tile click."""
        global last_tile_clicked
        last_tile_clicked = self.id


class ChessApp(App[None]):
    """Chess in the Terminal, but a little bit fancier."""

    TITLE = "Chess"
    BINDINGS: ClassVar = [
        ("ctrl+q", "quit_app", "Quit the app."),
        ("ctrl+n", "new_game", "Start a new game."),
        ("ctrl+r", "random_game", "Start a new random game."),
    ]
    CSS_PATH = (
        f"{Path(__file__).parent}/styles.css"
        if "__file__" in globals()
        else "styles.css"
    )

    def compose(self: "ChessApp") -> ComposeResult:
        """Generate screen widgets."""
        yield Header()
        with Horizontal(id="ui_container"):
            with Container(id="board"):
                for rank in range(8, 0, -1):
                    with Horizontal(id=f"rank_{rank}", classes="rank"):
                        yield Static(f"[b]{rank}[/b] ", classes="rank_label")
                        for file in FILES:
                            sq = f"{file}{rank}"
                            yield Tile(
                                id=sq,
                                classes=(
                                    f"{'black' if sq in BLACK_SQUARES else 'white'}"
                                    "_tile tile"
                                ),
                            )
                yield Static("[b]  a b c d e f g h [/b]")
            with Container(id="input_container"):
                yield Static("[b]COLOR[/b] to move.", id="to_move")
                yield Input(
                    placeholder="Enter your move in algebraic notation.",
                    id="move_input",
                )
                with Horizontal(id="buttons_container"):
                    yield Button("Move", id="move", variant="success")
                    yield Button("Offer Draw", id="offer_draw", variant="warning")
                    yield Button("Claim Draw", id="claim_draw", variant="warning")
                    yield Button("Resign", id="resign", variant="error")
            with Container(id="game_over_container"):
                yield Static("[b]COLOR[/b] won the game.", id="outcome")
                yield Static("Moves: ", id="moves")
                with Horizontal(id="game_over_buttons"):
                    yield Button("Play Another Game", id="play_another")
                    yield Button("Copy Moves", id="copy_moves")
            with Container(id="offer_draw_container"):
                yield Static(
                    "[b]COLOR[/b] offered a draw. Does [b]COLOR[/b] accept?",
                    id="offer_draw_label",
                )
                with Horizontal(id="offer_draw_buttons"):
                    yield Button("Yes", id="yes_draw", variant="success")
                    yield Button("No", id="no_draw", variant="error")
            with Container(id="promote_pawn_container"):
                yield Static(
                    "[b]Promote the pawn at square '  '.[/b]", id="promote_pawn_label"
                )
                with Horizontal():
                    yield Button("Queen", id="queen", classes="promote_button")
                    yield Button("Bishop", id="bishop", classes="promote_button")
                with Horizontal():
                    yield Button("Rook", id="rook", classes="promote_button")
                    yield Button("Knight", id="knight", classes="promote_button")
        yield Footer()

    def on_mount(self: "ChessApp") -> None:
        """Set up game."""
        if "random" in argv:
            self.reset(random=True)
        else:
            self.reset()

    def reset(self: "ChessApp", *, random: bool = False) -> None:
        """Reset the game."""
        global last_tile_clicked
        if not random:
            self.board = ChessBoard()
            self.is_random = False
        if random:
            self.board = ChessBoard(empty=True)
            self.board.set_random()
            self.is_random = True
        self.tile_selected: str | None = None
        last_tile_clicked = None
        self.query_one(
            "#game_over_container", expect_type=Container
        ).styles.display = "none"
        self.query_one("#moves", expect_type=Static).update("[b]Moves: [/b]")
        self.query_one("#outcome", expect_type=Static).update(
            "[b]COLOR[/b] won the game."
        )
        self.query_one(
            "#input_container", expect_type=Container
        ).styles.display = "block"
        self.query_one(
            "#offer_draw_container", expect_type=Container
        ).styles.display = "none"
        self.query_one("#offer_draw_label", expect_type=Static).update(
            "[b]COLOR[/b] offered a draw. Does [b]COLOR[/b] accept?"
        )
        self.query_one("#promote_pawn_container").styles.display = "none"
        self.update()

    def update(self: "ChessApp") -> None:
        """Update board display and turn."""
        status = self.board.status
        winning_king: str | None = None
        checkmated_king: str | None = None
        if status.winner is not None:
            winning_king = getattr(self.board, f"_{status.winner}_king_sq")
        if status.description == "checkmate":
            checkmated_king = getattr(
                self.board,
                f"_{'white' if status.winner == 'black' else 'black'}_king_sq",
            )
        for sq in self.board:
            self.set_tile(
                sq,
                self.board[sq],
                is_checkmated_king=(checkmated_king == sq),
                is_winning_king=(winning_king == sq),
            )
            self.query_one(f"#{sq}", expect_type=Tile).remove_class(
                "highlighted", "clicked_piece"
            )
        self.query_one("#to_move", expect_type=Static).update(
            f"[b]{self.board.turn.upper()}[/b] to move."
        )
        if status.game_over:
            self.query_one(
                "#game_over_container", expect_type=Container
            ).styles.display = "block"
            self.query_one("#play_another", expect_type=Button).focus()
            self.query_one(
                "#input_container", expect_type=Container
            ).styles.display = "none"
            self.query_one(
                "#offer_draw_container", expect_type=Container
            ).styles.display = "none"
            if status.winner is not None:
                self.query_one("#outcome", expect_type=Static).update(
                    f"[b]{status.winner.upper()}[/b] won the game "
                    f"by {status.description.replace('_', ' ')}."
                    if status.description is not None
                    else f"[b]{status.winner.upper()}[/b] won the game."
                )
            else:
                self.query_one("#outcome", expect_type=Static).update(
                    "The game ended in a [b]DRAW[/b] by "
                    f"{status.description.replace('_', ' ')}."
                    if status.description is not None
                    else "The game ended in a [b]DRAW[/b]."
                )
            self.query_one("#moves", expect_type=Static).update(
                f"[b]Moves:[/b] {self.board.export_moves()}"
            )
        self.tile_selected = None
        for sq in self.board:
            self.query_one(f"#{sq}", expect_type=Tile).remove_class(
                "highlighted", "clicked_piece"
            )
        if self.board.can_claim_draw():
            self.query_one("#offer_draw", expect_type=Button).styles.display = "none"
            self.query_one("#claim_draw", expect_type=Button).styles.display = "block"
        else:
            self.query_one("#offer_draw", expect_type=Button).styles.display = "block"
            self.query_one("#claim_draw", expect_type=Button).styles.display = "none"

    def set_tile(
        self: "ChessApp",
        square: str,
        piece: Piece | None,
        *,
        is_checkmated_king: bool = False,
        is_winning_king: bool = False,
    ) -> None:
        """Set a tile to empty or to a piece."""
        tile = self.query_one(f"#{square}", expect_type=Static)
        tile.remove_class("white_piece", "black_piece", "winning_king")
        if piece is None:
            tile.update("  ")
        else:
            tile.update(
                f"{PIECE_SYMBOLS[piece.piece_type]}{'#' if is_checkmated_king else ' '}"
            )
            tile.add_class(
                "winning_king" if is_winning_king else f"{piece.color}_piece"
            )

    @property
    def can_click_to_highlight(self: "ChessApp") -> bool:
        """Return True if click to highlight is enabled."""
        return not any(
            self.query_one(f"#{cnt}").styles.display == "block"
            for cnt in (
                "offer_draw_container",
                "game_over_container",
                "promote_pawn_container",
            )
        )

    def action_quit_app(self: "ChessApp") -> None:
        """Quit the app."""
        self.exit()

    def action_new_game(self: "ChessApp") -> None:
        """Start a new game."""
        self.reset()

    def action_random_game(self: "ChessApp") -> None:
        """Start a new game of Fischer random chess / Chess960."""
        self.reset(random=True)

    def submit_move(self: "ChessApp", move: str) -> None:
        """Submit a move."""
        try:
            self.board.move(move)
        except Exception as exc:
            self.notify(str(exc), severity="error")
        self.update()

    @on(Input.Submitted)
    def enter_move(self: "ChessApp", _: Input.Submitted | None = None) -> None:
        """Submit a move."""
        input_widget = self.query_one("#move_input", expect_type=Input)
        self.submit_move(input_widget.value)
        input_widget.value = ""

    def on_button_pressed(self: "ChessApp", event: Button.Pressed) -> None:
        """Handle button press."""
        match event.button.id:
            case "move":
                self.enter_move()
            case "offer_draw":
                self.offer_draw()
            case "claim_draw":
                self.accept_draw()
            case "resign":
                self.resign()
            case "play_another":
                self.reset(random=self.is_random)
            case "yes_draw":
                self.accept_draw()
            case "no_draw":
                self.decline_draw()
            case "copy_moves":
                try:
                    pyperclip.copy(self.board.export_moves())
                    self.notify("Moves copied to clipboard.")
                except Exception:
                    self.notify("Unable to copy moves to clipboard.", severity="error")
            case "queen" | "bishop" | "rook" | "knight":
                sq = re.search(
                    r"'([a-h1-8]{2})'",
                    str(
                        self.query_one(
                            "#promote_pawn_label", expect_type=Static
                        ).renderable
                    ),
                ).group(1)  # type: ignore
                self.board.promote_pawn(square=sq, piece_type=event.button.id)
                self.update()
                self.query_one("#promote_pawn_container").styles.display = "none"
                self.query_one("#input_container").styles.display = "block"

    def offer_draw(self: "ChessApp") -> None:
        """Offer a draw."""
        self.query_one(
            "#input_container", expect_type=Container
        ).styles.display = "none"
        self.query_one(
            "#offer_draw_container", expect_type=Container
        ).styles.display = "block"
        self.query_one("#offer_draw_label", expect_type=Static).update(
            f"[b]{self.board.turn.upper()}[/b] offered a draw. "
            f"Does [b]{'BLACK' if self.board.turn == 'white' else 'WHITE'}[/b] accept?"
        )

    def accept_draw(self: "ChessApp") -> None:
        """Accept an offered draw."""
        self.board.draw()
        self.update()

    def decline_draw(self: "ChessApp") -> None:
        """Decline an offered draw."""
        self.query_one(
            "#input_container", expect_type=Container
        ).styles.display = "block"
        self.query_one(
            "#offer_draw_container", expect_type=Container
        ).styles.display = "none"

    def resign(self: "ChessApp") -> None:
        """Resign."""
        self.board.resign()
        self.update()

    def on_click(self: "ChessApp", event: Click) -> None:
        """Handle tile click."""
        global last_tile_clicked
        if last_tile_clicked is None or not self.can_click_to_highlight:
            return None
        # If the same tile had been selected before the click, unselect the tile,
        # unless the tile is a king, and that king can be castled without moving.
        if self.tile_selected == last_tile_clicked and not (
            self.board.pieces[self.tile_selected].piece_type == "king"
            and self.tile_selected in ("c1", "c8", "g1", "g8")
            or (
                "highlighted"
                in self.query_one(f"#{self.tile_selected}", expect_type=Tile).classes
            )
        ):
            self.query_one(f"#{self.tile_selected}", expect_type=Tile).remove_class(
                "clicked_piece"
            )
            for sq in self.board:
                self.query_one(f"#{sq}", expect_type=Tile).remove_class("highlighted")
            self.tile_selected = None
            return None
        # If another piece of the same color was last clicked, and that piece
        # is not a rook involved in a castling move, switch
        # self.tile_selected to the new tile.
        if (
            self.tile_selected is not None
            and self.board[last_tile_clicked] is not None
            and "highlighted"
            not in self.query_one(f"#{last_tile_clicked}", expect_type=Tile).classes
            and self.board.pieces[last_tile_clicked].color == self.board.turn
        ):
            self.query_one(f"#{self.tile_selected}", expect_type=Tile).remove_class(
                "clicked_piece"
            )
            for sq in self.board:
                self.query_one(f"#{sq}", expect_type=Tile).remove_class("highlighted")
            self.tile_selected = last_tile_clicked
            self.query_one(f"#{self.tile_selected}", expect_type=Tile).add_class(
                "clicked_piece"
            )
            for sq in self.board.legal_moves(self.tile_selected):
                self.query_one(f"#{sq}", expect_type=Tile).add_class("highlighted")
            self.query_one(f"#{self.tile_selected}", expect_type=Tile).add_class(
                "clicked_piece"
            )
            return None
        # If no tile had been selected before the click, select the tile if possible.
        if (
            self.tile_selected is None
            and last_tile_clicked is not None
            and self.board[last_tile_clicked] is not None
            and self.board.pieces[last_tile_clicked].color == self.board.turn
        ):
            self.tile_selected = last_tile_clicked
            self.query_one(f"#{self.tile_selected}", expect_type=Tile).add_class(
                "clicked_piece"
            )
            for sq in self.board.legal_moves(self.tile_selected):
                self.query_one(f"#{sq}", expect_type=Tile).add_class("highlighted")
            return None
        # If a tile was selected and another tile is now selected,
        # check if it's a valid move. If so, make the move.
        if (
            self.tile_selected is not None
            and last_tile_clicked in self.board.legal_moves(self.tile_selected)
        ):
            self.board.move_piece(
                self.tile_selected,
                last_tile_clicked,
                allow_castle_and_en_passant=True,
                ignore_turn=True,
            )
            self.update()

            # Open the pawn promotion dialog if applicable.
            if self.board.pieces[
                last_tile_clicked
            ].piece_type == "pawn" and last_tile_clicked[1] in ("1", "8"):
                self.query_one(
                    "#input_container", expect_type=Container
                ).styles.display = "none"
                self.query_one(
                    "#promote_pawn_container", expect_type=Container
                ).styles.display = "block"
                self.query_one("#promote_pawn_label", expect_type=Static).update(
                    f"[b]Promote the pawn at square '{last_tile_clicked}'.[/b]"
                )

            self.tile_selected = None


def main() -> None:
    """Run app."""
    app = ChessApp()
    app.run()


if __name__ == "__main__":
    main()
