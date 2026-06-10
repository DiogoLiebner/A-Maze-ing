import typing

from .error_handle import InvalidConfig, ImpossibleMaze, BadSyntax
from .maze_utils import get_stamp_bounds


REQUIRED_KEYS = {"width", "height", "entry", "exit", "output_file", "perfect"}


class MazeConfig(typing.TypedDict):
    """Validated configuration parameters for maze generation.

    Constructed exclusively by ``read_config()`` after all values have
    been parsed, validated, and converted to their internal representations.
    Coordinates are stored 0-based internally regardless of how they are
    written in the config file.

    Attributes
    ----------
    width : int
        Maze width in logical cells.
    height : int
        Maze height in logical cells.
    entry : tuple[int, int]
        Start position as (row, col), 0-based.
    exit : tuple[int, int]
        End position as (row, col), 0-based.
    output_file : str
        Path to the ``.txt`` file where the maze will be written.
    perfect : bool
        If ``True``, no loops are added and the maze has a unique solution.
    seed : int or None
        Optional random seed for reproducible maze generation.
    stamp_warning : str or None
        Warning message set when the maze is too small for the 42 stamp,
        ``None`` otherwise.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    stamp_warning: str | None


def parse_coordinate(
        value: str,
        key: str,
        width: int,
        height: int
        ) -> tuple[int, int]:
    """Parse and validate a coordinate string from the config file.

    Expects a ``"x, y"`` formatted string where x is the column and y is
    the row, both 1-based for user convenience. Converts to 0-based
    (row, col) internally before returning.

    Parameters
    ----------
    value : str
        The raw coordinate string from the config file, e.g. ``"3, 5"``.
    key : str
        The config key name (e.g. ``"entry"`` or ``"exit"``), used in
        error messages to identify which coordinate failed validation.
    width : int
        Maze width in logical cells, used to validate the x bound.
    height : int
        Maze height in logical cells, used to validate the y bound.

    Returns
    -------
    tuple[int, int]
        The validated coordinate as a 0-based ``(row, col)`` tuple.

    Raises
    ------
    BadSyntax
        If ``value`` is not in ``"x, y"`` format or the values are not
        integers.
    ImpossibleMaze
        If the coordinate is outside the bounds of the maze dimensions.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise BadSyntax(
            f"'{key}' must be in format x, y. Not '{value}'"
        )

    try:
        col, row = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise BadSyntax(
            f"'{key}' coordinates must be integers. Got '{value}'"
        )

    # Config coordinates are 1-based for user convenience. Convert to 0-based.
    if not (0 <= col < width) or not (0 <= row < height):
        raise ImpossibleMaze(
            f"'{key}' coordinates ({col}, {row}) out of bounds for maze size "
            f"{width}x{height}"
        )

    return (row, col)


def read_config(
        filename: str = "config.txt"
        ) -> MazeConfig:
    """Read, parse, and validate a maze configuration file.

    Parses a plain-text ``KEY=VALUE`` config file line by line, validates
    all required keys and their values, resolves coordinates from 1-based
    to 0-based, and returns a fully validated ``MazeConfig``.

    Blank lines and lines beginning with ``#`` are treated as comments
    and ignored. Keys are case-insensitive. The following keys are
    required:

    - ``WIDTH``       : Maze width in logical cells (positive integer).
    - ``HEIGHT``      : Maze height in logical cells (positive integer).
    - ``ENTRY``       : Start coordinate in ``"x, y"`` format, 1-based.
    - ``EXIT``        : End coordinate in ``"x, y"`` format, 1-based.
    - ``OUTPUT_FILE`` : Path to the output ``.txt`` file.
    - ``PERFECT``     : ``"true"`` / ``"1"`` for a perfect maze, anything
                        else for a maze with loops.

    The following key is optional:

    - ``SEED`` : Integer seed for reproducible maze generation.

    Parameters
    ----------
    filename : str, optional
        Path to the configuration file. Defaults to ``"config.txt"``.

    Returns
    -------
    MazeConfig
        A fully validated ``MazeConfig`` TypedDict ready for use by
        ``generate_maze()``.

    Raises
    ------
    InvalidConfig
        If the file is not found, required keys are missing, or
        ``output_file`` does not end with ``.txt``.
    ImpossibleMaze
        If ``WIDTH`` or ``HEIGHT`` are not positive, entry and exit are
        the same cell, or either coordinate falls inside the 42 stamp
        region on a sufficiently large maze.
    BadSyntax
        If any line is missing ``=``, has an empty key or value, or a
        field that expects a number receives a non-integer string.
    """

    config: dict[str, str] = {}

    try:
        file = open(filename, "r")
    except FileNotFoundError:
        raise InvalidConfig(f"File '{filename}' not found")

    with file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise BadSyntax(
                    f"Line {line_num} is missing '=': '{line}'"
                )

            parts: list[str] = line.split("=", 1)
            key, value = parts[0].strip().lower(), parts[1].strip()
            if not key:
                raise BadSyntax(
                    f"Line {line_num} has an empty key: '{line}'"
                )
            if not value:
                raise BadSyntax(
                    f"Line {line_num} has an empty value: '{line}'"
                )
            config[key] = value

    missing: set[str] = REQUIRED_KEYS - config.keys()
    if missing:
        raise InvalidConfig(f"Missing required keys: {missing}")

    try:
        height: int = int(config["height"])
    except ValueError:
        raise BadSyntax("HEIGHT must be an integer")

    try:
        width: int = int(config["width"])
    except ValueError:
        raise BadSyntax("WIDTH must be an integer")

    if height <= 0 or width <= 0:
        raise ImpossibleMaze("WIDTH and HEIGHT must be positive integers")

    stamp_warning: str | None = None
    if height <= 5 or width <= 7:
        stamp_warning = "Warning: Maze too small for 42 pattern"

    if not config["output_file"].endswith(".txt"):
        raise InvalidConfig(
            f"'output_file' must be a .txt file, got '{config['output_file']}'"
        )

    entry: tuple[int, int] = parse_coordinate(
        config["entry"],
        "entry",
        width,
        height)
    exit: tuple[int, int] = parse_coordinate(
        config["exit"],
        "exit",
        width,
        height)

    if entry == exit:
        raise ImpossibleMaze("'ENTRY' and 'EXIT' cannot be the same")

    top, bottom, left, right = get_stamp_bounds(height, width)
    if stamp_warning is None:
        for coord, name in [(entry, "entry"), (exit, "exit")]:
            if top <= coord[0] <= bottom and left <= coord[1] <= right:
                raise ImpossibleMaze(
                    f"'{name.upper()}' coordinate ({coord[1]}, "
                    f"{coord[0]}) cannot be inside the 42 stamp"
                )

    if config["perfect"].lower() not in ("true", "false", "1", "0"):
        raise BadSyntax("PERFECT must be 'true' or 'false'")

    perfect: bool = config["perfect"].lower() in ("true", "1")

    seed: int | None = None
    if "seed" in config:
        try:
            seed = int(config["seed"])
        except ValueError:
            raise BadSyntax("SEED must be an integer")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=config["output_file"],
        perfect=perfect,
        seed=seed,
        stamp_warning=stamp_warning
    )
