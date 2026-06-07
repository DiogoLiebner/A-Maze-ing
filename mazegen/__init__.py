# mazegen/__init__.py

"""
mazegen — procedural maze generation and pathfinding package.

Public API
----------
read_config : Parse and validate a maze configuration file.
generate_maze : Generate a maze grid using iterative backtracking.
find_path : Solve a maze using A*.
write_output : Serialise the maze and solution path to a file.

Exceptions
----------
MazeError : Base class for all mazegen exceptions.
InvalidConfig : Raised for missing or structurally invalid config files.
ImpossibleMaze : Raised for logically contradictory maze parameters.
BadSyntax : Raised for malformed config file syntax.
"""

from .reading import read_config, MazeConfig
from .maze_generation import generate_maze
from .pathfinder import find_path
from .outputwrite import write_output
from .error_handle import BadSyntax, ImpossibleMaze, InvalidConfig, MazeError

__all__ = [
    "read_config",
    "MazeConfig",
    "generate_maze",
    "find_path",
    "write_output",
    "BadSyntax",
    "ImpossibleMaze",
    "InvalidConfig",
    "MazeError",
]

__version__ = "1.0.0"
