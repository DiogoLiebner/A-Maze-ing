# main.py
from srcs.reading import read_config, MazeConfig
from srcs.maze_generation import generate_maze
from srcs.pathfinder import find_path
from srcs.outputwrite import write_output
from srcs.error_handle import MazeError, ImpossibleMaze, InvalidConfig, BadSyntax


def print_maze(
    grid: list[list[int]],
    path: list[tuple[int, int]] | None,
    config: MazeConfig,
) -> None:
    """
    Print the maze to the terminal with the solution path overlaid.

    Symbols:
        █  = wall
        ·  = solution path
        S  = start
        E  = end
           = open cell

    Args:
        grid:   The 2D maze grid from generate_maze().
        path:   The solution path from find_path(), or None.
        config: The validated MazeConfig for start and end positions.
    """
    start: tuple[int, int] = config["entry"]
    end:   tuple[int, int] = config["exit"]

    path_cells: set[tuple[int, int]] = set()
    if path:
        for maze_r, maze_c in path:
            path_cells.add((2 * maze_r + 1, 2 * maze_c + 1))

    start_grid: tuple[int, int] = (2 * start[0] + 1, 2 * start[1] + 1)
    end_grid:   tuple[int, int] = (2 * end[0] + 1,   2 * end[1] + 1)

    for r, row in enumerate(grid):
        line: str = ""
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start_grid:
                line += "S"
            elif pos == end_grid:
                line += "E"
            elif pos in path_cells:
                line += "·"
            elif cell == 2:
                line += "\033[96m█\033[0m"
            elif cell == 1:
                line += "█"
            else:
                line += " "
        print(line)


def main() -> None:
    """
    Main entry point — reads config, generates maze,
    finds path, prints to terminal and writes output file.
    """
    try:
        cfg = read_config("config.txt")
        maze = generate_maze(cfg)
        path = find_path(maze, cfg)
        print_maze(maze, path, cfg)
        if path:
            print(f"\nPath found! {len(path)} steps.")
            print(f"Attempting to write to: {cfg['output_file']}")
            write_output(maze, cfg, path)
            print(f"Output written to {cfg['output_file']}")
        else:
            print("\nNo path found.")

    except MazeError as e:
        print(e)


if __name__ == "__main__":
    main()
