import subprocess
import os
import sys
from reading import MazeConfig, read_config
from maze_generation import generate_maze
from pathfinder import find_path
from outputwrite import write_output
from error_handle import MazeError


def main() -> None:
    cfg_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"

    config = read_config(cfg_file)

    grid = generate_maze(config)

    write_output(grid, config["output_file"])

    subprocess.run(["./maze_viewer", config["output_file"]], check=True)


if __name__ == "__main__":
    try:
        main()
    except MazeError as e:
        print(f"Error: {e}")
        sys.exit(1)
