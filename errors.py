from typing import Any, Optional


class Colors():
    """ANSI codes for coloring and formatting console output.

    Attributes:
        HEADER: Colored headers.
        OKBLUE: Blue text.
        OKCYAN: Cyan text.
        OKGREEN: Green text.
        WARNING: Orange/yellow text for warnings.
        FAIL: Red text for errors.
        ENDC: Resets the color.
        BOLD: Makes the text bold.
        UNDERLINE: Underlines the text.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Error(Exception):
    """Base class for parsing errors."""

    def msg(self, type: str, message: str) -> Any:
        """Format an error message with a type.

        Args:
            type: The error type.
            message: The error message.

        Returns:
            str: The formatted message with color.
        """
        error = Colors.FAIL + "[" + type + "]" + Colors.ENDC
        return error + message


class ParsingError(Exception):
    """Raised when parsing errors are found in the file."""


class MapFileError(Exception):
    """Raised when a map file parsing error occurs."""

    def __init__(self, line: int) -> None:
        """Initialize the exception with the error line number.

        Args:
            line: The line number where the error was detected.
        """
        self.line = line

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error_type = (
                f'{Colors.FAIL}'
                f'{Colors.BOLD}'
                f'[MapFileError] '
                f'{Colors.ENDC}'
                f'{Colors.BOLD}'
        )
        return error_type + f"Line {self.line}: " + Colors.ENDC

    @staticmethod
    def msg(message: str, line: Optional[int] = None) -> Any:
        """Create a formatted error message.

        Args:
            message: The error message text.
            line: The optional line number.

        Returns:
            str: The formatted message with colors.
        """
        error = Colors.FAIL + Colors.BOLD + "[MapFileError] " + Colors.ENDC
        if line:
            error += Colors.BOLD + f'Line {line}: '
        return error + Colors.ENDC + message

    @staticmethod
    def warning(line: int, message: str) -> Any:
        """Create a formatted warning message.

        Args:
            line: The line number in the file.
            message: The warning message text.

        Returns:
            str: The formatted warning message with colors.
        """
        warning = (
                f'{Colors.WARNING}'
                f'{Colors.BOLD}'
                f'[MapFileWarning] '
                f'{Colors.ENDC}'
                f'{Colors.BOLD}'
                f'Line {line}: '
        )
        return warning + message + Colors.ENDC


class HubError(MapFileError):
    """Raised when a hub definition is invalid."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize the exception with the line number and message.

        Args:
            line: The error line number.
            message: Detailed description of the hub error.
        """
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + self.message


class MetadataError(MapFileError):
    """Raised when metadata is invalid."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize the exception with the line number and message.

        Args:
            line: The error line number.
            message: Description of the metadata error.
        """
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + self.message


class InvalidKeyError(MapFileError):
    """Raised when an invalid key is found in the file."""

    def __init__(self, line: int, key: str) -> None:
        """Initialize the exception with the line number and invalid key.

        Args:
            line: The error line number.
            key: The invalid key detected.
        """
        self.key = key
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        if len(self.key):
            return error + f"Invalid <{self.key}> key definition"
        else:
            return error + "Invalid key definition"


class InvalidLineError(MapFileError):
    """Raised when a line contains too many arguments."""

    def __init__(self, line: int) -> None:
        """Initialize the exception with the line number.

        Args:
            line: The line number containing too many arguments.
        """
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + "Too many arguments"


class InvalidValue(MapFileError):
    """Raised when a value is invalid."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize the exception with the line number and message.

        Args:
            line: The error line number.
            message: Description of the invalid value.
        """
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + self.message


class DoublonError(MapFileError):
    """Raised when an element is defined twice."""

    def __init__(self, line: int, key: str) -> None:
        """Initialize the exception with the line number and duplicate key.

        Args:
            line: The error line number.
            key: The duplicated key.
        """
        self.key = key
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + f"Already defined earlier '{self.key}'"


class ConnectionError(MapFileError):
    """Raised when a connection definition is invalid."""

    def __init__(self, line: int, message: str) -> None:
        """Initialize the exception with the line number and message.

        Args:
            line: The error line number.
            message: Description of the connection error.
        """
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        """Return the formatted error message."""
        error = super().__str__()
        return error + self.message


class SimulationStop(Exception):
    """Raised when the user stops the simulation (Ctrl+C)."""

    def __init__(self) -> None:
        """Initialize the exception with a formatted message."""
        self.template = (
                f'{Colors.WARNING}'
                f'{Colors.BOLD}'
                f'[SimulationState] '
                f'{Colors.ENDC}'
        )

    def __str__(self) -> Any:
        """Return the formatted exception message."""
        return self.template + "Simulation stopped"
