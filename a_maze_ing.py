import subprocess
import sys
import os
from mazegen import (
    read_config,
    find_path,
    generate_maze,
    write_output,
    MazeError
)


def main() -> None:
    cfg_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"

    no_launch = "--no-launch" in sys.argv

    config = read_config(cfg_file)

    grid = generate_maze(config)

    path = find_path(grid, config)
    if path is None:
        raise MazeError("No path found from ENTRY to EXIT")

    write_output(grid, config, path)
<<<<<<< HEAD
    subprocess.run(["./maze_viewer", config["output_file"]], check=True)
    os.remove(config["output_file"])
=======
    if not no_launch:
        subprocess.run(["./maze_viewer", config["output_file"]], check=True)
>>>>>>> refs/remotes/origin/main


if __name__ == "__main__":
    try:
        main()
    except MazeError as e:
        print(f"Error: {e}")
        sys.exit(1)
