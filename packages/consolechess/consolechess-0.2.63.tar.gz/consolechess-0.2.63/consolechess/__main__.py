"""Play a game of chess in the terminal."""

from importlib.util import find_spec
from sys import argv

from . import __version__, asciiconsole

RICH_AVAILABLE = find_spec("rich") is not None

if RICH_AVAILABLE:
    from . import console

TEXTUAL_AVAILABLE = find_spec("textual") is not None

if TEXTUAL_AVAILABLE:
    from . import tui


def main() -> None:
    """Start chess."""
    args = " ".join(argv)
    if "-v" in args:
        print(f"consolechess {__version__}")
    elif (
        "ascii" in args
        or "-a" in args
        or (not RICH_AVAILABLE and not TEXTUAL_AVAILABLE)
    ):
        asciiconsole.main()
    elif RICH_AVAILABLE and (
        " console" in args or "-c" in args or not TEXTUAL_AVAILABLE
    ):
        console.main()
    elif TEXTUAL_AVAILABLE:
        tui.main()
    else:
        asciiconsole.main()


if __name__ == "__main__":
    main()
