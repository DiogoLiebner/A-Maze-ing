import subprocess
import sys
from mazegen import (
    read_config,
    find_path,
    generate_maze,
    write_output,
    MazeError
)


def main() -> None:
    cfg_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"

    config = read_config(cfg_file)

    grid = generate_maze(config)

    path = find_path(grid, config)
    write_output(grid, config, path)

    subprocess.run(["./maze_viewer", config["output_file"]], check=True)


if __name__ == "__main__":
    try:
        main()
    except MazeError as e:
        print(f"Error: {e}")
        sys.exit(1)
