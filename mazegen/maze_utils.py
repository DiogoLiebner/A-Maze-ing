"""Utility functions for maze generation and validation."""


_DIGIT_4 = [
    "1 0 0",
    "1 0 0",
    "1 1 1",
    "0 0 1",
    "0 0 1"
]

_DIGIT_2 = [
    "1 1 1",
    "0 0 1",
    "1 1 1",
    "1 0 0",
    "1 1 1",
]


def _parse_digit(pattern: list[str]) -> list[list[int]]:
    return [[int(v) for v in row.split()] for row in pattern]


def get_stamp_bounds(height: int, width: int) -> tuple[int, int, int, int]:
    """
    Returns the bounds of the 42 stamp as (top, bottom, left, right).
    Coordinates are in maze cell space (not grid space).
    """
    digit_h = len(_parse_digit(_DIGIT_4))
    digit_w = len(_parse_digit(_DIGIT_4)[0])
    spacing = 1
    total_w = digit_w + spacing + digit_w

    start_lr = height // 2 - digit_h // 2
    start_lc = width // 2 - total_w // 2

    top = start_lr
    bottom = start_lr + digit_h - 1
    left = start_lc
    right = start_lc + total_w - 1

    return (top, bottom, left, right)
