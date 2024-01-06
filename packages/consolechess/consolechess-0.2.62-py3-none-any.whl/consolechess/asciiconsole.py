"""An ASCII game of chess in the console."""

from sys import argv

from .board import ChessBoard


def main() -> None:
    """Play a game of chess in the console."""
    board = ChessBoard()
    if "random" in argv:
        board.set_random()
    game_over = False
    exception_last_move: Exception | None = None
    while not game_over:
        print("\n")
        board.print(plaintext=True)
        print(f"\n{board.turn.upper()} to move.\n")
        can_claim_draw = board.can_claim_draw()
        if exception_last_move is not None:
            print(f"{exception_last_move}\n")
            exception_last_move = None
        move = input(
            "Enter your move in algebraic chess notation.\n"
            f"Enter 'draw' to {'claim' if can_claim_draw else 'offer'} draw.\n"
            "Enter 'resign' to resign.\n\nYour input: "
        ).strip()
        if move == "draw":
            if can_claim_draw:
                board.draw()
            else:
                accepted = input(
                    f"\n{board.turn.upper()} offered a draw. Do you accept? [yes/no]: "
                )
                print("\n")
                if "y" in accepted:
                    board.draw()
        elif move == "resign":
            board.resign()
        else:
            try:
                board.move(move)
            except Exception as exc:
                exception_last_move = exc
        game_over = board.status.game_over
    status = board.status
    if status.winner is None:
        print(
            f"\nThe game ended in a DRAW by {status.description.replace('_', ' ')}.\n"
            if status.description is not None
            else "\nThe game ended in a DRAW.\n"
        )
    else:
        print(
            f"\n{status.winner.upper()} won the game "
            f"by {status.description.replace('_', ' ')}.\n"
            if status.description is not None
            else f"\n{status.winner.upper()} won the game.\n"
        )
    print(f"Moves: {board.export_moves()}")
    play_again = input("\nPlay again? [yes/no]: ")
    if "y" in play_again:
        main()
