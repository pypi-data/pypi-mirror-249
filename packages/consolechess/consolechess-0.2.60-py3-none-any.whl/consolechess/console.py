"""A game of chess in the console."""

from sys import argv

from rich.console import Console
from rich.prompt import Prompt
from rich.rule import Rule

from .board import ChessBoard
from .datatypes import GameStatus


def main() -> None:
    """Start a game of chess in the terminal."""
    console = Console()
    board = ChessBoard()
    if "random" in argv:
        board.set_random()
    result: GameStatus | None = None
    last_move_exception: Exception | None = None
    while result is None:
        board.print()
        console.print(Rule())
        if board.turn == "white":
            console.print("[reverse][bold]WHITE[/bold][/reverse] to move.")
        else:
            console.print("[bold]BLACK[/bold] to move.")
        if last_move_exception is not None:
            console.print(f"\n[red]{last_move_exception}[/red]")
            last_move_exception = None
        can_claim_draw = board.can_claim_draw()
        console.print(
            "\n[b]Enter your move in algrebraic chess notation.[/b]\n"
            f"Enter 'draw' to {'claim' if can_claim_draw else 'offer'} draw."
            "\nEnter 'resign' to resign.\n"
        )
        move = Prompt.ask("Enter your move")
        print("\n")
        if move == "resign":
            board.print()
            board.resign()
            result = board.status
            winner = result.winner
            description = result.description
            assert winner is not None
            console.print(
                f"{winner.upper()} won the game by {description}."
                if description is not None
                else f"{winner.upper()} won the game."
            )
            print(f"Moves: {board.export_moves()}\n")
        elif move == "draw":
            if not can_claim_draw:
                response = Prompt.ask(
                    "[bold]"
                    f"{'WHITE' if board.turn == 'white' else 'BLACK'}"
                    "[/bold] offered a draw. Does "
                    f"{'WHITE' if board.turn == 'black' else 'BLACK'}"
                    " accept?",
                    choices=["yes", "no"],
                )
                print("\n")
            if can_claim_draw or response == "yes":
                board.print()
                console.print(
                    "The game ended in a [b]DRAW[/b] "
                    f"by {board.status.description.replace('_', ' ')}."
                    if board.status.description is not None
                    else "The game ended in a [b]DRAW[/b]."
                )
                board.draw()
                print(f"Moves: {board.export_moves()}\n")
                result = board.status
        else:
            try:
                board.move(move)
            except Exception as exc:
                last_move_exception = exc
            if board.status.game_over:
                board.print()
                result = board.status
                if (winner := result.winner) is not None:
                    console.print(
                        f"[b]{winner.upper()}[/b] won the game "
                        f"by {result.description.replace('_', ' ')}."
                        if result.description is not None
                        else f"{winner.upper()} won the game."
                    )
                else:
                    console.print(
                        "The game ended in a [b]DRAW[/b] "
                        f"by {board.status.description.replace('_', ' ')}."
                        if board.status.description is not None
                        else "The game ended in a [b]DRAW[/b]."
                    )
                print(f"Moves: {board.export_moves()}\n")


if __name__ == "__main__":
    main()
