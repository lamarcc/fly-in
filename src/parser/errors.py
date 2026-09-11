from typing import Any, Optional


class Colors():
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
    def msg(self, type: str, message: str) -> Any:
        error = Colors.FAIL + "[" + type + "]" + Colors.ENDC
        return error + message


class ParsingError(Exception):
    pass


class MapFileError(Exception):
    def __init__(self, line: int) -> None:
        self.line = line

    def __str__(self) -> Any:
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
        error = Colors.FAIL + Colors.BOLD + "[MapFileError] " + Colors.ENDC
        if line:
            error += Colors.BOLD + f'Line {line}: '
        return error + Colors.ENDC + message

    @staticmethod
    def warning(line: int, message: str) -> Any:
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
    def __init__(self, line: int, message: str) -> None:
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + self.message


class MetadataError(MapFileError):
    def __init__(self, line: int, message: str) -> None:
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + self.message


class InvalidKeyError(MapFileError):
    def __init__(self, line: int, key: str) -> None:
        self.key = key
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        if len(self.key):
            return error + f"Invalid <{self.key}> key definition"
        else:
            return error + "Invalid key definition"


class InvalidLineError(MapFileError):
    def __init__(self, line: int) -> None:
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + "Too much arguments"


class InvalidValue(MapFileError):
    def __init__(self, line: int, message: str) -> None:
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + self.message


class DoublonError(MapFileError):
    def __init__(self, line: int, key: str) -> None:
        self.key = key
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + f"Already defined earlier '{self.key}'"


class ConnectionError(MapFileError):
    def __init__(self, line: int, message: str) -> None:
        self.message = message
        super().__init__(line)

    def __str__(self) -> Any:
        error = super().__str__()
        return error + self.message


class SimulationStop(Exception):
    def __init__(self) -> None:
        self.template = (
                f'{Colors.WARNING}'
                f'{Colors.BOLD}'
                f'[SimulationState] '
                f'{Colors.ENDC}'
        )

    def __str__(self) -> Any:
        return self.template + "Simulation stopped"
