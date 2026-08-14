class bcolors:
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
        error = bcolors.FAIL + "[" + type + "]" +  bcolors.ENDC
        return error + message


class MapFileError(Exception):
    def __init__(self, line):
        self.line = line

    def __str__(self):
        error_type = bcolors.FAIL + bcolors.BOLD + "[MapFileError] " + bcolors.ENDC
        return error_type + bcolors.BOLD + f"Line {self.line}: "

    def test(self):
        self.t.append(self.__str__())

    def msg(line, message):
        error = bcolors.FAIL + bcolors.BOLD + "[MapFileError] " + bcolors.ENDC + bcolors.BOLD + f"Line {line}: "
        return error + message

    def warning(line, message):
        warning = bcolors.WARNING + bcolors.BOLD + "[MapFileWarning] " + bcolors.ENDC + bcolors.BOLD + f"Line {line}: "
        return warning + message

class HubError(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message


class MetadataError(MapFileError):
    def __init__(self, line, key):
        self.key = key
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + f"Unknown metadata '{self.key}'"


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


class InvalidDronesValue(MapFileError):
    def __init__(self, line, message):
        self.message = message
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + self.message


class DoublonError(MapFileError):
    def __init__(self, line, key):
        super().__init__(line)

    def __str__(self):
        error = super().__str__()
        return error + f"Already defined earlier '{self.key}'"
