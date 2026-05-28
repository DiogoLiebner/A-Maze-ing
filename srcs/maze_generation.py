import random
from .reading import MazeConfig


_DIGIT_4 = [
    "1 0 0 0 0",
    "1 0 0 0 0",
    "1 0 0 0 0",
    "1 1 1 1 1",
    "0 0 0 0 1",
    "0 0 0 0 1",
    "0 0 0 0 1"
]

_DIGIT_2 = [
    "1 1 1 1 1",
    "0 0 0 0 1",
    "0 0 0 0 1",
    "1 1 1 1 1",
    "1 0 0 0 0",
    "1 0 0 0 0",
    "1 1 1 1 1",
]


def _parse_digit(pattern: list[str]) -> list[list[str]]:
    return [[int(v) for v in row.split()] for row in pattern]


def _stamp_42(grid: list[list[int]]) -> tuple[int, int, int, int]:
    rows = len(grid)
    cols = len(grid[0])

    digit_4 = _parse_digit(_DIGIT_4)
    digit_2 = _parse_digit(_DIGIT_2)

    digit_h = len(digit_4)
    digit_w = len(digit_4[0])
    spacing = 2
    total_w = digit_w * 2 + spacing
    total_h = digit_h

    start_r = ((rows - total_h) // 2) & ~1
    start_c = ((cols - total_w) // 2) & ~1

    def stamp_digit(
        pattern: list[list[int]],
        offset_c: int
    ) -> None:
        for r in range(digit_h):
            for c in range(digit_w):
                gr = start_r + r
                gc = start_c + offset_c + c
                if (0 <= gr < rows and 0 <= gc < cols):
                    if pattern[r][c] == 1:
                        grid[gr][gc] = 2
                    else:
                        grid[gr][gc] = 0

    stamp_digit(digit_4, 0)
    stamp_digit(digit_2, digit_w + spacing)

    return start_r, start_c, digit_h, total_w


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

                wall_r = 2 * current_r + 1 + dr
                wall_c = 2 * current_c + 1 + dc
                if grid[wall_r][wall_c] == 1:
                    grid[2 * nr + 1][2 * nc + 1] = 0
                    grid[wall_r][wall_c] = 0
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
            if grid[r][c] == 2:
                continue
            if grid[r][c] == 0 and grid[r][c + 1] == 0:
                candidate_walls.append((r, c))
            if grid[r][c] == 0 and grid[r + 1][c] == 0:
                candidate_walls.append((r, c))

    random.shuffle(candidate_walls)
    remove_count: int = int(len(candidate_walls) * loop_factor)

    for r, c in candidate_walls[:remove_count]:
        if grid[r][c] != 2:
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
    start_r, start_c, digit_h, total_w = _stamp_42(grid)

    visited: set[tuple[int, int]] = set()
    for r in range(height):
        for c in range(width):
            gr, gc = 2 * r + 1, 2 * c + 1
            if (0 <= gr < len(grid) and 0 <= gc < len(grid[0]) and
                    grid[gr][gc] == 2):
                visited.add((r, c))

    _carve_passages(grid, entry[0], entry[1], height, width, visited)

    grid[2 * exit[0] + 1][2 * exit[1] + 1] = 0

    if not perfect:
        _add_loops(grid, loop_factor)

    return grid
