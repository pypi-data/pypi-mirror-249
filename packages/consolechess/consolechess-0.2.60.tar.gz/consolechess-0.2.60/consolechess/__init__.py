"""A game of chess."""

from pkg_resources import get_distribution

__version__ = get_distribution("consolechess").version

from . import board  # noqa: F401
