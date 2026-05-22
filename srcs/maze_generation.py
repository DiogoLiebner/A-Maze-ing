import random
from .reading import MazeConfig


def _build_grid(width: int, height: int) -> list[list[str]]:
    """
        Initializes the maze grid with walls and spaces.
    """
    rows: int = 2 * height + 1
    cols: int = 2 * width + 1
    return [[1] * cols for _ in range(rows)]


def _carve_passages(
        grid: list[list[int]],
        row: int,
        col: int,
        height: int,
        width: int,
        visited: set[tuple[int, int]]
        ) -> None:
    """
        Carves passages in the grid using a depth-first search algorithm.
    """
    stack: list[tuple[int, int]] = [(row, col)]
    visited.add((row, col))

    grid[2 * row + 1][2 * col + 1] = 0

    directions: list[tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        current_r, current_c = stack[-1]

        random.shuffle(directions)

        carved: bool = False
        for dr, dc in directions:
            nr, nc = current_r + dr, current_c + dc

            if (0 <= nr < height)\
                    and (0 <= nc < width) and (nr, nc) not in visited:

                grid[2 * nr + 1][2 * nc + 1] = 0
                grid[2 * current_r + 1 + dr][2 * current_c + 1 + dc] = 0

                visited.add((nr, nc))
                stack.append((nr, nc))
                carved = True
                break

        if not carved:
            stack.pop()


def _add_loops(grid: list[list[int]], loop_factor: float) -> None:
    """
        Randomly adds loops to the maze by removing some walls.
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    candidate_walls: list[tuple[int, int]] = []

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] == 0 and grid[r][c + 1] == 0:
                candidate_walls.append((r, c))
            if grid[r][c] == 0 and grid[r + 1][c] == 0:
                candidate_walls.append((r, c))

    random.shuffle(candidate_walls)
    remove_count: int = int(len(candidate_walls) * loop_factor)

    for r, c in candidate_walls[:remove_count]:
        grid[r][c] = 0


def generate_maze(
        config: MazeConfig,
        loop_factor: float = 0.1
        ) -> list[list[int]]:
    width: int = config["width"]
    height: int = config["height"]
    entry: tuple[int, int] = config["entry"]
    exit: tuple[int, int] = config["exit"]
    perfect: bool = config["perfect"]

    grid: list[list[int]] = _build_grid(width, height)
    visited: set[tuple[int, int]] = set()

    _carve_passages(grid, entry[0], entry[1], height, width, visited)

    grid[2 * exit[0] + 1][2 * exit[1] + 1] = 0

    if not perfect:
        _add_loops(grid, loop_factor)

    return grid
