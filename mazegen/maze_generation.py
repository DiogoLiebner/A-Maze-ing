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
    """Stamp a '42' pattern into the centre of the maze grid.

    The digits '4' and '2' are defined as 5-row pixel patterns and placed
    side by side in the middle of the logical maze space. Stamped cells are
    set to value 2 and returned as a set of maze coordinates so the passage
    carver treats them as pre-visited, preserving the shape.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid to stamp into. Modified in place.
    height : int
        The maze height in logical cells (not grid rows).
    width : int
        The maze width in logical cells (not grid cols).

    Returns
    -------
    set[tuple[int, int]]
        A set of (row, col) maze-coordinate tuples that were stamped,
        to be passed to ``_carve_passages`` as pre-visited cells.
    """

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
        """Stamp a single digit pattern onto the grid at a column offset.

        Iterates over the pixel pattern and, for each active pixel (value 1),
        writes value 2 to the corresponding grid cell and records the logical
        maze coordinate in the enclosing ``stamped`` set.

        Parameters
        ----------
        pattern : list[list[int]]
            A 2D list of 0/1 pixels representing the digit shape.
        offset_lc : int
            Column offset in logical maze coordinates, used to position
            the digit relative to ``start_lc``.

        Returns
        -------
        None
        """

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
    """Initialise a blank maze grid with all cells set to walls.

    The grid uses a 2:1 scaling where each logical maze cell at position
    (r, c) maps to grid position (2r+1, 2c+1), and the cells between
    them represent walls that can be carved open. All cells are
    initialised to 1 (wall).

    Parameters
    ----------
    width : int
        The maze width in logical cells.
    height : int
        The maze height in logical cells.

    Returns
    -------
    list[list[int]]
        A 2D list of shape ``(2*height+1, 2*width+1)`` filled with 1s.
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
    Carve passages through the grid using iterative depth-first search.

    Implements the iterative backtracking algorithm. Starting from
    (row, col), a stack tracks the current path. At each step an
    unvisited neighbour is chosen at random and the wall between the
    current cell and that neighbour is removed (set to 0). If no
    unvisited neighbours remain the algorithm backtracks by popping
    the stack, continuing until the stack is empty.

    Cells already present in ``visited`` (e.g. stamped cells) are
    never carved into, which preserves the stamp shape while allowing
    the rest of the maze to connect around it.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid to carve into. Modified in place.
    row : int
        Starting row in logical maze coordinates.
    col : int
        Starting column in logical maze coordinates.
    height : int
        Maze height in logical cells, used for bounds checking.
    width : int
        Maze width in logical cells, used for bounds checking.
    visited : set[tuple[int, int]]
        Set of already-visited logical maze coordinates. Stamped cells
        should be added here before calling this function.

    Returns
    -------
    None

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


def _would_create_3x3(grid: list[list[int]], r: int, c: int) -> bool:
    """
    Check if removing the wall at (r, c) would create a 3x3 open area.
    """
    for dr in range(-2, 1):
        for dc in range(-2, 1):
            all_open = True
            for tr in range(3):
                for tc in range(3):
                    gr = 2 * ((r - 1) // 2 + dr + tr) + 1
                    gc = 2 * ((c - 1) // 2 + dc + tc) + 1
                    if not (0 <= gr < len(grid) and 0 <= gc < len(grid[0])):
                        all_open = False
                        break
                    if grid[gr][gc] != 0:
                        all_open = False
                        break
                    if tc < 2 and grid[gr][gc + 2] != 0:
                        all_open = False
                        break
                    if tr < 2 and grid[gr + 2][gc] != 0:
                        all_open = False
                        break
            if all_open:
                return True
    return False


def _add_loops(grid: list[list[int]], loop_factor: float) -> None:
    """Introduce random loops by selectively removing interior walls.

    Collects candidate walls — cells that sit directly between two open
    passage cells — then removes a random subset of them based on
    ``loop_factor``. Only true between-cell walls are considered:

    - Vertical walls:   odd row, even col (separates left/right neighbours).
    - Horizontal walls: even row, odd col (separates top/bottom neighbours).

    Even-even intersection points are never removed as doing so would
    create shortcuts that bypass cells entirely.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid to modify in place.
    loop_factor : float
        Fraction of candidate walls to remove, in the range [0.0, 1.0].
        Higher values produce more loops. At least 1 wall is always
        removed when candidates exist.

    Returns
    -------
    None
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

            if r % 2 == 1 and c % 2 == 0:
                if grid[r][c - 1] == 0 and grid[r][c + 1] == 0:
                    candidate_walls.append((r, c))
            elif r % 2 == 0 and c % 2 == 1:
                if grid[r - 1][c] == 0 and grid[r + 1][c] == 0:
                    candidate_walls.append((r, c))

    random.shuffle(candidate_walls)
    remove_count: int = max(1, int(len(candidate_walls) * loop_factor))

    for r, c in candidate_walls[:remove_count]:
        if grid[r][c] == 1:
            grid[r][c] = 0
        if _would_create_3x3(grid,r , c):
            grid[r][c] = 1


def generate_maze(
        config: MazeConfig,
        loop_factor: float = 0.1,
        ) -> list[list[int]]:
    """Generate a maze grid from the given configuration.

    Orchestrates the full maze generation pipeline:

    1. Build a blank walled grid of size ``(2*height+1) x (2*width+1)``.
    2. Stamp the '42' pattern into the centre if the maze is large enough
       (height > 5 and width > 7).
    3. Seed the random number generator if a seed is provided.
    4. Carve passages using iterative backtracking, treating stamped cells
       as pre-visited so the pattern is preserved.
    5. Force the entry and exit cells open.
    6. Optionally introduce loops when ``perfect`` is ``False``.

    Parameters
    ----------
    config : MazeConfig
        A ``MazeConfig`` TypedDict containing the following keys:

        - ``width``   (int)            : Maze width in logical cells.
        - ``height``  (int)            : Maze height in logical cells.
        - ``entry``   (tuple[int,int]) : Start position (row, col), 0-based.
        - ``exit``    (tuple[int,int]) : End position (row, col), 0-based.
        - ``perfect`` (bool)           : If ``True``, no loops are added.
        - ``seed``    (int | None)     : Optional seed for reproducibility.

    loop_factor : float, optional
        Fraction of candidate walls to remove when ``perfect`` is ``False``.
        Must be in the range [0.0, 1.0]. Defaults to ``0.1``.
        Has no effect when ``perfect`` is ``True``.

    Returns
    -------
    list[list[int]]
        A 2D list representing the maze grid where:
        - ``0`` = open passage
        - ``1`` = wall
        - ``2`` = stamped '42' decoration cell (open to the pathfinder)
    """
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
