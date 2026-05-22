from reading import MazeConfig


def _encode_cell(
          grid: list[list[int]],
          maze_r: int,
          maze_c: int
        ) -> str:
    gr: int = 2 * maze_r + 1
    gc: int = 2 * maze_c + 1

    north: int = grid[gr - 1][gc]
    east: int = grid[gr][gc + 1]
    south: int = grid[gr + 1][gc]
    west: int = grid[gr][gc - 1]

    value: int = (north << 0) | (east << 1) | (south << 2) | (west << 3)

    return format(value, 'X')


def _path_to_directions(path: list[tuple[int, int]]) -> str:
    directions: list[str] = []

    for i in range(len(path) - 1):
        curr_r, curr_c = path[i]
        next_r, next_c = path[i + 1]

        dr: int = next_r - curr_r
        dc: int = next_c - curr_c

    if dr == -1:
        directions.append("N")
    elif dr == 1:
        directions.append("S")
    elif dc == 1:
        directions.append("E")
    elif dc == -1:
        directions.append("W")

    return "".join(directions)


def write_output(
            grid: list[list[int]],
            config: MazeConfig,
            path: list[tuple[int, int]]
        ) -> None:

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
        f.write(f"{entry[1]},{entry[0]}\n")
        f.write(f"{exit[1]},{exit[0]}\n")
        f.write(_path_to_directions(path) + "\n")
