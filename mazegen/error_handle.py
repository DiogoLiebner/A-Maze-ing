class MazeError(Exception):
    """
    Base class for all maze-related exceptions.

    All custom exceptions in this package inherit from ``MazeError``,
    allowing callers to catch any maze error with a single ``except``
    clause if needed.

    Parameters
    ----------
    message : str, optional
        Human-readable description of the error.
        Defaults to ``"AN ERROR OCCURRED!"``.

    Attributes
    ----------
    message : str
        The error message passed at construction.
    """
    def __init__(self, message: str = "AN ERROR OCCURRED!") -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"MazeError: {self.message}"


class InvalidConfig(MazeError):
    """
    Raised when the configuration file is missing or structurally invalid.

    Use this exception for errors that prevent the config from being read
    at all — such as a missing file, absent required keys, or an output
    file with the wrong extension. For errors in the values themselves,
    use ``BadSyntax`` or ``ImpossibleMaze`` instead.

    Parameters
    ----------
    message : str, optional
        Human-readable description of the configuration error.
        Defaults to ``"Invalid configuration in config.txt!"``.
    """

    def __init__(
            self,
            message: str = "Invalid configuration in config.txt!"
    ) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidConfig: {self.message}"


class ImpossibleMaze(MazeError):
    """
    Raised when configuration values produce a maze that cannot be built.

    Use this exception when the values are syntactically valid but logically
    contradictory — such as non-positive dimensions, entry equal to exit,
    or coordinates that fall inside the reserved stamp region.

    Parameters
    ----------
    message : str, optional
        Human-readable description of why the maze is impossible.
        Defaults to ``"The maze has impossible parameters!"``.
    """
    def __init__(
            self,
            message: str = "The maze has impossible parameters!"
    ) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"ImpossibleMaze: {self.message}"


class BadSyntax(MazeError):
    """
    Raised when a config file line cannot be parsed due to bad syntax.

    Use this exception when a line is present but malformed — such as a
    missing ``=`` separator, an empty key or value, or a field that expects
    a number but receives a non-integer string.

    Parameters
    ----------
    message : str, optional
        Human-readable description of the syntax error.
        Defaults to ``"Syntax error in config.txt!"``.
    """
    def __init__(self, message: str = "Syntax error in config.txt!") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"BadSyntax: {self.message}"
