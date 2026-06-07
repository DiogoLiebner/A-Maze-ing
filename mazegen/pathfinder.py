import heapq
from .reading import MazeConfig


def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Estimate the distance between two grid positions using Manhattan
    distance.

    Used by A* as an admissible heuristic — it never overestimates the true
    cost on a grid where only orthogonal movement is allowed, guaranteeing
    that the shortest path is always found.

    Parameters
    ----------
    a : tuple[int, int]
        The current position as a (row, col) grid coordinate.
    b : tuple[int, int]
        The target position as a (row, col) grid coordinate.

    Returns
    -------
    int
        The Manhattan distance between ``a`` and ``b``.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _to_grid_coords(maze_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Convert a logical maze position to its 2:1 scaled grid coordinate.

    The maze grid uses a 2:1 scaling where each logical cell at position
    (r, c) maps to grid position (2r+1, 2c+1). The surrounding cells
    represent walls between logical cells.

    Parameters
    ----------
    maze_pos : tuple[int, int]
        A (row, col) position in logical maze coordinates.

    Returns
    -------
    tuple[int, int]
        The corresponding (row, col) position in grid coordinates.
    """
    return (2 * maze_pos[0] + 1, 2 * maze_pos[1] + 1)


def _to_maze_coords(grid_pos: tuple[int, int]) -> tuple[int, int]:
    """Convert a 2:1 scaled grid position back to logical maze coordinates.

    Reverses the scaling applied by ``_to_grid_coords``. Only valid for
    grid positions where both row and col are odd (actual maze cell centres);
    wall cells between them do not have a meaningful maze coordinate.

    Parameters
    ----------
    grid_pos : tuple[int, int]
        A (row, col) position in grid coordinates. Both values should be odd.

    Returns
    -------
    tuple[int, int]
        The corresponding (row, col) position in logical maze coordinates.
    """
    return ((grid_pos[0] - 1) // 2, (grid_pos[1] - 1) // 2)


def find_path(
        grid: list[list[int]],
        config: MazeConfig
        ) -> list[tuple[int, int]] | None:
    """Find the shortest path through the maze from entry to exit using A*.

    Runs A* on the full 2:1 scaled grid, expanding cells by their combined
    actual cost ``g(n)`` and Manhattan distance heuristic ``h(n)``. Once the
    exit is reached, the path is reconstructed from the ``came_from`` map and
    filtered to only include logical maze cell centres (odd row and odd col),
    then converted back to maze coordinates before being returned.

    Parameters
    ----------
    grid : list[list[int]]
        The 2D maze grid produced by ``generate_maze()``, where:
        - ``0`` = open passage
        - ``1`` = wall
        - ``2`` = stamped decoration cell (treated as open)

    config : MazeConfig
        A validated ``MazeConfig`` TypedDict containing at minimum:
        - ``entry`` (tuple[int, int]) : Start position (row, col), 0-based.
        - ``exit``  (tuple[int, int]) : End position (row, col), 0-based.

    Returns
    -------
    list[tuple[int, int]] or None
        A list of (row, col) logical maze coordinate tuples representing
        the shortest path from entry to exit, inclusive of both endpoints.
        Returns ``None`` if no path exists between entry and exit.
    """
    entry: tuple[int, int] = config["entry"]
    exit: tuple[int, int] = config["exit"]

    grid_entry: tuple[int, int] = _to_grid_coords(entry)
    grid_exit: tuple[int, int] = _to_grid_coords(exit)

    rows: int = len(grid)
    cols: int = len(grid[0])

    open_set: list[tuple[int, tuple[int, int]]] = []
    heapq.heappush(open_set, (0, grid_entry))

    came_from: dict[
            tuple[int, int],
            tuple[int, int] | None
        ] = {grid_entry: None}

    g_score: dict[tuple[int, int], int] = {grid_entry: 0}

    directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == grid_exit:
            path: list[tuple[int, int]] = []
            step: tuple[int, int] | None = current

            while step is not None:
                r, c = step
                if r % 2 == 1 and c % 2 == 1:
                    path.append(_to_maze_coords(step))
                step = came_from[step]

            path.reverse()
            return path

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            neighbour: tuple[int, int] = (nr, nc)

            if (0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == 0):

                tent_g: int = g_score[current] + 1

                if neighbour not in g_score or tent_g < g_score[neighbour]:
                    g_score[neighbour] = tent_g
                    f_score: int = tent_g + _heuristic(neighbour, grid_exit)
                    heapq.heappush(open_set, (f_score, neighbour))
                    came_from[neighbour] = current

    return None
