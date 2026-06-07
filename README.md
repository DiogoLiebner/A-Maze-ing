*This project has been created as part of the 42 curriculum by dlima-li, rafmonte.*

# AMazeing

A maze generation and pathfinding tool written in Python, with a C/MiniLibX graphical visualizer. The core logic lives in a standalone, reusable Python package (`mazegen`) and the visualizer is a compiled C binary driven by MiniLibX on Linux.

---

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
  - [Requirements](#requirements)
  - [Build \& Run](#build--run)
  - [Makefile Targets](#makefile-targets)
  - [Using a Virtual Environment](#using-a-virtual-environment)
- [Project Structure](#project-structure)
- [Config File Format](#config-file-format)
- [Maze Generation — Iterative Backtracking](#maze-generation--iterative-backtracking)
- [Pathfinding — A\*](#pathfinding--a)
- [Reusable Package — `mazegen`](#reusable-package--mazegen)
- [Display \& Controls](#display--controls)

---

## Description

AMazeing procedurally generates mazes using an **iterative backtracking** algorithm and solves them with **A\***. The result is rendered in a MiniLibX window where the user can interact with the maze in real time — toggling the solution path, cycling colour themes, and generating new mazes on the fly.

The project is split into two independent layers:

- **`mazegen/`** — a pure Python package that handles generation, pathfinding, configuration reading, and output writing. It is fully reusable and installable via pip.
- **`MiniLibX/`** — a C program that reads the maze output and renders it graphically using the MiniLibX library.

---

## Instructions

### Requirements

**Python side**
- Python 3.x
- `venv` (standard library)
- `flake8` and `mypy` (installed automatically by `make`)

**C / MiniLibX side**
- `gcc` / `cc`
- X11 development libraries:
  ```bash
  sudo apt install libx11-dev libxext-dev   # Debian/Ubuntu
  ```
- MiniLibX Linux (included under `MiniLibX/minilibx-linux/`)

---

### Build & Run

Build everything (MiniLibX binary + Python venv) and launch:

```bash
make run
```

This single command:
1. Compiles the MiniLibX library
2. Compiles the `maze_viewer` C binary
3. Creates a Python virtual environment under `venv/`
4. Installs `mazegen` in editable mode (`pip install -e .`)
5. Installs `flake8` and `mypy`
6. Runs `a_maze_ing.py` with `config.txt`

To build without running:

```bash
make
```

To run with verbose Python output (useful for debugging):

```bash
make debug
```

---

### Makefile Targets

| Target | Description |
|---|---|
| `make` / `make all` | Build MiniLibX, compile `maze_viewer`, create venv |
| `make install` | Create venv and install dependencies only |
| `make run` | Build everything, then run the program |
| `make debug` | Build everything, then run with unbuffered output (`-u`) |
| `make clean` | Remove `maze_viewer` binary and all `__pycache__` / `.pyc` files |
| `make lint` | Run `flake8` + `mypy` with standard settings |
| `make lint-strict` | Run `flake8` + `mypy --strict` |

---

### Using a Virtual Environment

The Makefile manages the venv automatically, but you can also work with it directly:

```bash
# Create and activate the venv manually
python3 -m venv venv
source venv/bin/activate

# Install mazegen in editable mode (changes to source reflect immediately)
pip install -e .

# Run
python3 a_maze_ing.py config.txt

# Deactivate when done
deactivate
```

> **Note for evaluators:** The `mazegen` package is designed to be installed and tested inside a virtual environment. Install it via the wheel or in editable mode, then import it directly in your own scripts — no path manipulation required.
>
> ```bash
> pip install mazegen-1.0.0-py3-none-any.whl
> # or
> pip install mazegen-1.0.0.tar.gz
> ```

---

## Project Structure

```
AMazeing/
├── a_maze_ing.py                   # Main entry point — ties Python and C together
├── config.txt                      # Runtime configuration file
├── Makefile                        # Builds MiniLibX, venv, and runs the program
├── README.md
├── mazegen-1.0.0.tar.gz            # Source distribution
├── mazegen-1.0.0-py3-none-any.whl  # Wheel distribution
│
├── mazegen/                        # Reusable Python package (see below)
│   ├── __init__.py
│   ├── error_handle.py             # Custom error/exception handling
│   ├── maze_generation.py          # Iterative backtracking maze generator
│   ├── maze_utils.py               # Shared grid and cell utilities
│   ├── outputwrite.py              # Writes maze to file for the C visualizer
│   ├── pathfinder.py               # A* pathfinding implementation
│   └── reading.py                  # Parses config.txt
│
└── MiniLibX/                       # C graphical visualizer
    ├── minilibx-linux/             # MiniLibX library source
    ├── MLXmain.c                   # Window setup, event loop, key hooks
    ├── render.c                    # Drawing logic (walls, path, colours)
    ├── parser.c                    # Reads maze file output from Python
    ├── ft_split.c                  # String splitting utility
    ├── get_next_line.c             # Line-by-line file reader
    └── get_next_line_utils.c       # GNL helper functions
```

---

## Config File Format

The program is configured via `config.txt`, passed as the first argument to `a_maze_ing.py`. Each line follows a `KEY=VALUE` format. Lines beginning with `#` are treated as comments.

```ini
# config.txt

WIDTH=21
HEIGHT=21
ENTRY=1,1
EXIT=20,20
OUTPUT_FILE=maze.txt
PERFECT=False

```

| Key | Type | Description |
|---|---|---|
| `WIDTH` | `int` (odd recommended) | Number of columns in the maze grid |
| `HEIGHT` | `int` (odd recommended) | Number of rows in the maze grid |
| `ENTRY` | `col,row` (1-based) | Starting point of the maze |
| `EXIT` | `col,row` (1-based) | Ending point of the maze
| `OUTPUT_FILE` | `str` (must end in `.txt`) | Path where the maze will be written for the C visualizer |
| `PERFECT` | `bool` (`true` or `false`) | Whether to generate a perfect maze (no loops) or an imperfect one (with loops) |
| `SEED` | `int` (optional) | Random seed for reproducible maze generation |

---

## Maze Generation — Iterative Backtracking

The maze is generated using **iterative backtracking** (also known as the recursive backtracker algorithm, implemented here without recursion to avoid stack limits on large mazes).

**How it works:**

1. Start with a grid where every cell is a wall.
2. Pick a starting cell, mark it as visited, and push it onto a stack.
3. While the stack is not empty:
   - Look at the current cell's neighbours (N, S, E, W) that are **unvisited**.
   - If any exist, pick one at random, carve a passage between the current cell and the chosen neighbour, mark it visited, and push it onto the stack.
   - If no unvisited neighbours exist, **backtrack** by popping the stack.
4. Repeat until the stack is empty — every cell has been visited and the maze is complete.

**Properties of the output:**
- Always produces a **perfect maze** — exactly one path exists between any two cells.
- No loops, no isolated regions.
- Tends to generate mazes with long, winding corridors and relatively few dead ends compared to other algorithms.

---

## Pathfinding — A*

The solver uses the **A\* (A-star)** algorithm to find the shortest path from the maze entrance to the exit.

**How it works:**

A\* maintains an open set of candidate cells, each scored by:

```
f(n) = g(n) + h(n)
```

- `g(n)` — the exact cost from the start to cell `n` (number of steps taken).
- `h(n)` — a heuristic estimate of the cost from `n` to the goal. This implementation uses the **Manhattan distance**: `|x_goal - x_n| + |y_goal - y_n|`, which is admissible on a grid with no diagonal movement.

At each step, the cell with the lowest `f(n)` is expanded. Once the goal is reached, the path is reconstructed by tracing parent pointers back to the start.

**Properties:**
- Guaranteed to find the **shortest path** when the heuristic is admissible (never overestimates).
- More efficient than Dijkstra on typical maze grids due to the directional heuristic.

---

## Reusable Package — `mazegen`

The entire `mazegen/` directory is a self-contained, installable Python package. It has no dependency on the C visualizer or MiniLibX and can be used independently in any Python project.

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

```python
from mazegen.maze_generation import generate_maze
from mazegen.pathfinder import solve
from mazegen.reading import read_config
from mazegen.outputwrite import write_maze
```

**Module breakdown:**

| Module | Responsibility |
|---|---|
| `maze_generation.py` | Iterative backtracking generator — returns a 2D grid |
| `pathfinder.py` | A\* solver — takes a grid, returns the solution path |
| `maze_utils.py` | Verifies 42 Stamp bounds |
| `outputwrite.py` | Serialises the maze grid to a file format readable by the C visualizer |
| `reading.py` | Parses `config.txt` into a usable config object |
| `error_handle.py` | Custom exceptions and error reporting |

> **For evaluators:** Install the package in a fresh virtual environment and import the modules directly. The package is tested in editable mode (`pip install -e .`) during development but the distributed `.whl` and `.tar.gz` are ready for isolated installation and testing.

---

## Display & Controls

Once the program is running, the maze is rendered in a MiniLibX window. The following keyboard controls are available:

| Key | Action |
|---|---|
| `1` – `9` | Cycle through colour themes for the maze display |
| `Space` | Toggle the A\* solution path on / off |
| `Enter` | Generate a new maze (same dimensions, new layout) |
| `Esc` | Exit the program |


## Roles of each team member ##

- **dlima-li**: Maze generation logic, A\* pathfinding, config parsing, error handling, file output format, Makefile, and Python package structure.

- **rafmonte**: C/MiniLibX visualizer and controls, event handling, rendering logic, and integration of the Python output with the C input.


## Planing of the project ##

By dividing the project into two layers (Python logic and C visualizer), we can work in parallel on both components. The Python package can be developed and tested independently, while the C visualizer can be built to read the maze output once the format is defined. While continuously improving the visualizer, the other parts of the project were being developed, like the Makefile, README, and packaging.
