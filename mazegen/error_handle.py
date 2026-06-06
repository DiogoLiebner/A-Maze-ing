class MazeError(Exception):
    """
        Base class for exceptions in this module.
    """
    def __init__(self, message: str = "AN ERROR OCCURRED!") -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"MazeError: {self.message}"


class InvalidConfig(MazeError):
    """
        Exception raised for errors in the config.txt file
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
        Exception raised when the maze has impossible parameters
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
        Exception raised for syntax errors in the config.txt file
    """
    def __init__(self, message: str = "Syntax error in config.txt!") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"BadSyntax: {self.message}"
