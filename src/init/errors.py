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
    def msg(self, type, message):
        error = Colors.FAIL + "[" + type + "]" + Colors.ENDC
        return error + message


class ParsingError(Exception):
    pass


class MapFileError(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        error_type = Colors.FAIL + Colors.BOLD + "[MapFileError] " + Colors.ENDC + Colors.BOLD
        return error_type + f"Line {self.line}: " + Colors.ENDC

    def msg(line, message):
        error = Colors.FAIL + Colors.BOLD + "[MapFileError] " + Colors.ENDC + Colors.BOLD + f"Line {line}: "
        return error + Colors.ENDC + message

    def warning(line, message):
        warning = Colors.WARNING + Colors.BOLD + "[MapFileWarning] " + Colors.ENDC + Colors.BOLD + f"Line {line}: "
        return warning + message + Colors.ENDC


class HubError(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message


class MetadataError(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message


class InvalidKeyError(MapFileError):
    def __init__(self, line, key):
        self.key = key
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + f"Invalid '{self.key}' map information"


class InvalidLineError(MapFileError):
    def __init__(self, line):
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + "Too much arguments"


class InvalidValue(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message


class DoublonError(MapFileError):
    def __init__(self, line, key):
        self.key = key
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + f"Already defined earlier '{self.key}'"


class ConnectionError(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message

class PathfindingError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        error_type = Colors.FAIL + Colors.BOLD + "[PathfindingError] " + Colors.ENDC + Colors.BOLD
        return error_type + self.message + Colors.ENDC
