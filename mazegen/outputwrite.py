from .reading import MazeConfig


def _encode_cell(
        grid: list[list[int]],
        maze_c: int,
        maze_r: int
        ) -> str:
    """Encode a single maze cell as a hexadecimal wall bitmask.

    Reads the four walls surrounding the logical cell at (maze_r, maze_c)
    and packs them into a 4-bit integer, where each bit represents whether
    the corresponding wall is present (1) or open (0):

    - Bit 0 (LSB) : North wall
    - Bit 1       : East wall
    - Bit 2       : South wall
    - Bit 3       : West wall

    The result is returned as a single uppercase hex character (0-F),
    giving the C parser a compact, unambiguous cell descriptor.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid produced by ``generate_maze()``.
    maze_c : int
        The logical column of the cell to encode, 0-based.
    maze_r : int
        The logical row of the cell to encode, 0-based.

    Returns
    -------
    str
        A single uppercase hexadecimal character representing the wall
        configuration of the cell.
    """
    gr: int = 2 * maze_r + 1
    gc: int = 2 * maze_c + 1

    # preserve stamp marker
    if grid[gr][gc] == 2:
        return 'Z'

    north: int = grid[gr - 1][gc]
    east: int = grid[gr][gc + 1]
    south: int = grid[gr + 1][gc]
    west: int = grid[gr][gc - 1]
    value: int = (north << 0) | (east << 1) | (south << 2) | (west << 3)
    return format(value, 'X')


def _path_to_directions(path: list[tuple[int, int]]) -> str:
    """Convert a sequence of maze coordinates into a cardinal direction string.

    Compares consecutive positions in the path and appends the corresponding
    compass direction for each step. The resulting string is consumed by the
    C parser to animate or display the solution path.

    Parameters
    ----------
    path : list[tuple[int, int]]
        An ordered list of (row, col) maze coordinates representing the
        solution path from entry to exit, as returned by ``find_path()``.

    Returns
    -------
    str
        A string of concatenated direction characters, one per step:

        - ``"N"`` : row decreased (moved north)
        - ``"S"`` : row increased (moved south)
        - ``"E"`` : col increased (moved east)
        - ``"W"`` : col decreased (moved west)

        Returns an empty string if the path has fewer than two positions.
    """
    directions: list[str] = []

    for i in range(len(path) - 1):
        curr_r, curr_c = path[i]
        next_r, next_c = path[i + 1]

        dr: int = next_r - curr_r
        dc: int = next_c - curr_c

        if dr < 0:
            directions.append("N")
        elif dr > 0:
            directions.append("S")
        elif dc > 0:
            directions.append("E")
        elif dc < 0:
            directions.append("W")
    return "".join(directions)


def write_output(
            grid: list[list[int]],
            config: MazeConfig,
            path: list[tuple[int, int]]
        ) -> None:
    """
    Write the maze, entry/exit positions, and solution path to a file.

    Serialises the maze into the format expected by the MiniLibX C parser:

    1. One hex-encoded row per maze row, each cell encoded as a single
       uppercase hex character representing its wall bitmask.
    2. A blank separator line.
    3. The entry coordinate as ``"col,row"`` in 1-based notation.
    4. The exit coordinate as ``"col,row"`` in 1-based notation.
    5. The solution path as a string of cardinal direction characters.

    Coordinates are written as 1-based because the C parser subtracts 1
    on read to convert back to 0-based indices.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid produced by ``generate_maze()``.
    config : MazeConfig
        A validated ``MazeConfig`` containing at minimum:

        - ``width``       (int)            :Maze width in logical cells.
        - ``height``      (int)            :Maze height in logical cells.
        - ``entry``       (tuple[int,int]) :Start position (row, col), 0-based.
        - ``exit``        (tuple[int,int]) :End position (row, col), 0-based.
        - ``output_file`` (str)            :Path to the output ``.txt`` file.

    path : list[tuple[int, int]]
        The solution path as an ordered list of (row, col) maze coordinates,
        as returned by ``find_path()``.

    Returns
    -------
    None
    """
    width: int = config["width"]
    height: int = config["height"]
    entry: tuple[int, int] = config["entry"]
    exit: tuple[int, int] = config["exit"]
    output_file: str = config["output_file"]

    with open(output_file, "w") as f:
        for maze_r in range(height):
            row_str: str = ""
            for maze_c in range(width):
                row_str += _encode_cell(grid, maze_c, maze_r)
            f.write(row_str + "\n")

        f.write("\n")
        f.write(f"{entry[1] + 1},{entry[0] + 1}\n")
        f.write(f"{exit[1] + 1},{exit[0] + 1}\n")
        f.write(_path_to_directions(path) + "\n")
