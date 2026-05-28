from .error_handle import InvalidConfig, ImpossibleMaze, BadSyntax
import typing


REQUIRED_KEYS = {"width", "height", "entry", "exit", "output_file", "perfect"}


# FUNCTION FOR MAZE READING TO SEE IF ITS PERFECT IS MISSING,
# NEEDS TO BE ADDED LATER


class MazeConfig(typing.TypedDict):
    """
        TypedDict for the maze configuration parameters.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def parse_coordinate(
        value: str,
        key: str,
        width: int,
        height: int
        ) -> tuple[int, int]:

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

    if not (1 <= col <= width) or not (1 <= row <= height):
        raise ImpossibleMaze(
            f"'{key}' coordinates ({col}, {row}) out of bounds for maze size \
{width}x{height}"
        )
    return (row - 1, col - 1)


def read_config(
        filename: str = "config.txt"
        ) -> MazeConfig:
    """
        Reads the maze configuration from a file and returns a
        dictionary with the parameters.
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

    if height <= 5 or width <= 7:
        raise ImpossibleMaze("Maze too small for 42 pattern")

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

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=config["output_file"],
        perfect=config["perfect"]
        # Need perfect bool function to define if maze is perfect or not
    )
