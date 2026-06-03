# mazegen

Maze generation package extracted from the **A-Maze-ing** project.

Generates perfect mazes (or imperfect ones with loops) using an iterative
depth-first search algorithm, with a "42" pattern stamped at the centre.

---

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

---

## Quick start

```python
from mazegen import read_config, generate_maze

config = read_config("config.txt")
grid = generate_maze(config)
```

---

## Config file format

```
# config.txt
width       = 20
height      = 15
entry       = 1,1
exit        = 20,15
output_file = maze.txt
perfect     = true
```

| Key | Type | Description |
|---|---|---|
| `width` | int | Number of columns (≥ 8) |
| `height` | int | Number of rows (≥ 6) |
| `entry` | `col,row` | Entry point, 1-based |
| `exit` | `col,row` | Exit point, 1-based |
| `output_file` | str | Must end in `.txt` |
| `perfect` | bool | `true` = no loops, `false` = loops added |

---

## Custom parameters

### Size and entry/exit via config

```python
from mazegen import MazeConfig, generate_maze

config = MazeConfig(
    width=30,
    height=20,
    entry=(0, 0),        # zero-based (row, col)
    exit=(19, 29),
    output_file="maze.txt",
    perfect=True,
)
grid = generate_maze(config)
```

### Seed — reproducible mazes

Pass `seed` directly to `generate_maze`:

```python
grid = generate_maze(config, seed=42)
```

Calling with the same seed always produces the same maze.

### Imperfect maze — adding loops

Set `perfect = false` in the config (or `perfect=False` inline) and
optionally tune `loop_factor` (0.0 to 1.0, default 0.1):

```python
config["perfect"] = False
grid = generate_maze(config, loop_factor=0.3, seed=7)
```

Higher `loop_factor` removes more walls and creates more alternate paths.

---

## Accessing the generated structure

`generate_maze` returns a `list[list[int]]` of size
`(2 * height + 1) × (2 * width + 1)`:

| Value | Meaning |
|---|---|
| `0` | Open passage |
| `1` | Wall |
| `2` | "42" pattern (open, decorative) |

Logical cell `(row, col)` maps to grid position `(2*row + 1, 2*col + 1)`:

```python
grid = generate_maze(config, seed=0)

# Check whether a logical cell is open
row, col = 3, 5
is_open = grid[2 * row + 1][2 * col + 1] == 0

# Check whether the passage between two horizontal neighbours is open
# (i.e. no wall between (3,5) and (3,6))
wall_open = grid[2 * row + 1][2 * col + 2] == 0

# Raw grid dimensions
print(len(grid))        # 2 * height + 1
print(len(grid[0]))     # 2 * width  + 1
```

---

## Accessing the solution

Use `find_path` to get the solution as a list of logical `(row, col)` cells
from entry to exit:

```python
from mazegen import MazeConfig, generate_maze, find_path

config = MazeConfig(
    width=20, height=15,
    entry=(0, 0), exit=(14, 19),
    output_file="maze.txt", perfect=True,
)
grid = generate_maze(config, seed=42)

path = find_path(grid, config["entry"], config["exit"])

print(f"Solution length: {len(path)} steps")
for row, col in path:
    print(f"  ({row}, {col})")
```

`find_path` returns a list of `(row, col)` tuples ordered from entry to exit,
or an empty list if no path exists.

---

## Saving the output

```python
from mazegen import read_config, generate_maze, write_output

config = read_config("config.txt")
grid = generate_maze(config, seed=0)
write_output(grid, config["output_file"])
```

---

## Error handling

| Exception | Raised when |
|---|---|
| `InvalidConfig` | File not found, missing keys, bad `output_file` extension |
| `ImpossibleMaze` | Maze too small, coordinates out of bounds, entry == exit |
| `BadSyntax` | Malformed config lines, non-integer values |
| `MazeError` | Base class for all of the above |

```python
from mazegen import read_config, InvalidConfig, ImpossibleMaze, BadSyntax

try:
    config = read_config("config.txt")
except (InvalidConfig, ImpossibleMaze, BadSyntax) as e:
    print(f"Config error: {e}")
```

---

## Rebuild from source

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install build
python -m build
# → dist/mazegen-1.0.0-py3-none-any.whl
# → dist/mazegen-1.0.0.tar.gz
```
