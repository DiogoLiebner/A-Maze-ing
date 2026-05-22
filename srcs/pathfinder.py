import heapq
from reading import MazeConfig


def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
        Manhattan distance heuristic for A*
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _to_grid_coords(maze_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Convert maze coordinates to 2:1 scaled grid coordinates.
    A maze position (r, c) maps to grid position (2r+1, 2c+1).

    Args:
        maze_pos: A (row, col) position in maze coordinates.

    Returns:
        The corresponding (row, col) position in grid coordinates
    """
    return (2 * maze_pos[0] + 1, 2 * maze_pos[1] + 1)


def _to_maze_coords(grid_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Convert 2:1 scaled grid coordinates back to maze coordinates.
    A grid position (r, c) maps to maze position ((r-1)//2, (c-1)//2).

    Args:
        grid_pos: A (row, col) position in grid coordinates.

    Returns:
        The corresponding (row, col) position in maze coordinates.
    """
    return ((grid_pos[0] - 1) // 2, (grid_pos[1] - 1) // 2)


def find_path(
        grid: list[list[int]],
        config: MazeConfig
        ) -> list[tuple[int, int]] | None:

    """
        Find the shortest path through the maze from start to end using A*.

        The path is returned in maze coordinates (not grid coordinates),
        so it maps directly back to the config's start and end values.

        Args:
            grid:   The 2D maze grid (0 = open, 1 = wall) from generate_maze().
            config: The validated MazeConfig containing
                                start and end positions.

        Returns:
            A list of (row, col) maze coordinate tuples representing the
            shortest path from start to end inclusive,
            or None if no path exists.
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
