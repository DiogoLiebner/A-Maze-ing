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
    """Parse a pixel pattern from a list of space-separated strings.

    Converts each row of a digit pattern from a whitespace-separated string
    of ``"0"`` and ``"1"`` characters into a list of integers. Used to
    prepare the ``_DIGIT_4`` and ``_DIGIT_2`` patterns for stamping.

    Parameters
    ----------
    pattern : list[str]
        A list of strings where each string is a space-separated row of
        pixel values, e.g. ``["1 0 1", "0 1 0"]``.

    Returns
    -------
    list[list[int]]
        A 2D list of integers (0 or 1) representing the digit pixel grid.
    """
    return [[int(v) for v in row.split()] for row in pattern]


def get_stamp_bounds(height: int, width: int) -> tuple[int, int, int, int]:
    """Return the bounding box of the '42' stamp in logical maze coordinates.

    Computes the top-left and bottom-right extents of the stamped '42'
    pattern based on the maze
    "1 0 0",
 dimensions. Used by ``read_config()`` to
    reject entry and exit coordinates that would overlap the stamp region,
    and by tests to verify stamp placement.

    All returned values are in logical maze cell space (not grid space),
    so they can be compared directly against ``MazeConfig`` entry/exit
    coordinates.

    Parameters
    ----------
    height : int
        Maze height in logical cells.
    width : int
        Maze width in logical cells.

    Returns
    -------
    tuple[int, int, int, int]
        A ``(top, bottom, left, right)`` tuple of inclusive bounds in
        logical maze coordinates:

        - ``top``    : First row occupied by the stamp.
        - ``bottom`` : Last row occupied by the stamp.
        - ``left``   : First column occupied by the stamp.
        - ``right``  : Last column occupied by the stamp.
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
