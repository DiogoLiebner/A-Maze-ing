import random
from .reading import MazeConfig
from .maze_utils import _parse_digit


_DIGIT_4 = [
    "1 0 0",
    "1 0 0",
    "1 1 1",
    "0 0 1",
    "0 0 1"
]

_DIGIT_2 = [
    "1 1 1",
    "0 0 1",
    "1 1 1",
    "1 0 0",
    "1 1 1",
]


def _stamp_42(
            grid: list[list[int]],
            height: int, width: int
        ) -> set[tuple[int, int]]:
    digit_4 = _parse_digit(_DIGIT_4)
    digit_2 = _parse_digit(_DIGIT_2)

    digit_h = len(digit_4)
    digit_w = len(digit_4[0])
    spacing = 1
    total_w = digit_w + spacing + digit_w

    start_lr = height // 2 - digit_h // 2
    start_lc = width // 2 - total_w // 2

    stamped: set[tuple[int, int]] = set()

    def stamp_digit(pattern: list[list[int]], offset_lc: int) -> None:
        for r in range(digit_h):
            for c in range(digit_w):
                lr = start_lr + r
                lc = start_lc + offset_lc + c
                gr = 2 * lr + 1
                gc = 2 * lc + 1
                if 0 <= gr < len(grid) and 0 <= gc < len(grid[0]):
                    if pattern[r][c] == 1:
                        grid[gr][gc] = 2
                        stamped.add((lr, lc))

    stamp_digit(digit_4, 0)
    stamp_digit(digit_2, digit_w + spacing)

    return stamped


def _build_grid(width: int, height: int) -> list[list[int]]:
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
        Randomly adds loops to the maze by removing valid between-cell walls.
        This avoids even-even intersection removals and can be more aggressive
        depending on loop_factor.
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    candidate_walls: list[tuple[int, int]] = []

    for r in range(2, rows - 2):
        for c in range(2, cols - 2):
            if grid[r][c] in (0, 2):
                continue
            if grid[r][c] != 1:
                continue

            # Only consider walls that separate two cells:
            # - vertical walls => odd row, even col
            # - horizontal walls => even row, odd col
            # Skip even-even intersection points, which can create
            # illegal teleport shortcuts when removed.
            if r % 2 == 1 and c % 2 == 0:
                if grid[r][c - 1] == 0 and grid[r][c + 1] == 0:
                    candidate_walls.append((r, c))
            elif r % 2 == 0 and c % 2 == 1:
                if grid[r - 1][c] == 0 and grid[r + 1][c] == 0:
                    candidate_walls.append((r, c))

    random.shuffle(candidate_walls)
    # Remove a larger share of valid candidate walls for more loops.
    remove_count: int = max(1, int(len(candidate_walls) * loop_factor))

    for r, c in candidate_walls[:remove_count]:
        if grid[r][c] == 1:
            grid[r][c] = 0


def generate_maze(
        config: MazeConfig,
        loop_factor: float = 0.1,
        ) -> list[list[int]]:

    width: int = config["width"]
    height: int = config["height"]
    entry: tuple[int, int] = config["entry"]
    exit: tuple[int, int] = config["exit"]
    seed: int | None = config.get("seed")

    grid: list[list[int]] = _build_grid(width, height)

    stamped: set[tuple[int, int]] = set()
    if height > 5 and width > 7:
        stamped = _stamp_42(grid, height, width)

    visited: set[tuple[int, int]] = stamped.copy()

    if seed is not None:
        random.seed(seed)

    _carve_passages(grid, 0, 0, height, width, visited)

    grid[2 * entry[0] + 1][2 * entry[1] + 1] = 0
    grid[2 * exit[0] + 1][2 * exit[1] + 1] = 0

    if config["perfect"] is False:
        _add_loops(grid, loop_factor)

    return grid
