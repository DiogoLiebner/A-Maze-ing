from error_handle import InvalidConfig, ImpossibleMaze, BadSyntax


REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

# create parse_coordinate function to parse the entry and exit coordinates

def read_config(filename: str = "config.txt") -> dict[str, int | str | tuple[int, int]]:
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
        raise ImpossibleMaze("Maze too small: minimum size is 8x6")

    if not config["output_file"].endswith(".txt"):
        raise InvalidConfig(
            f"'output_file' must be a .txt file, got '{config['output_file']}'"
        )

    entry: tuple[int, int] = parse_coordinate(config["entry"], "entry", width, height)
    exit: tuple[int, int] = parse_coordinate(config["exit"], "exit", width, height)

    if entry == exit:
        raise ImpossibleMaze("'ENTRY' and 'EXIT' cannot be the same")

    config["height"] = height
    config["width"] = width
    config["entry"] = entry
    config["exit"] = exit
    
    
    return config # type: ignore[return-value]
    # SO METI PARA NAO DAR MYPY ERROR NO FICHEIRO TODO
