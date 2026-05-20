class MazeError(Exception):
    """
        Base class for exceptions in this module.
    """
    def __init__(self, message="AN ERROR OCCURRED!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"MazeError: {self.message}"


class InvalidConfig(MazeError):
    """
        Exception raised for errors in the config.txt file
    """
    def __init__(self, message="Invalid configuration in config.txt!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"InvalidConfig: {self.message}"


class ImpossibleMaze(MazeError):
    """
        Exception raised when the maze has impossible parameters
    """
    def __init__(self, message="The maze has impossible parameters!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"ImpossibleMaze: {self.message}"


class BadSyntax(MazeError):
    """
        Exception raised for syntax errors in the config.txt file
    """
    def __init__(self, message="Syntax error in config.txt!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"BadSyntax: {self.message}"
