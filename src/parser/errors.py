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
    def __init__(self, line, message):
        self.line = line
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        error = bcolors.FAIL + bcolors.BOLD + "[MapFileError]" + bcolors.ENDC
        return error + bcolors.BOLD + f" Line {self.line}: {self.message}"

    def msg(line, message):
        error = bcolors.FAIL + bcolors.BOLD + "[MapFileError] " + bcolors.ENDC + bcolors.BOLD + f"Line {line}: "
        return error + message

    def warning(line, message):
            warning = bcolors.WARNING + bcolors.BOLD + "[MapFileWarning] " + bcolors.ENDC + bcolors.BOLD + f"Line {line}: "
            return warning + message

class HubError(MapFileError):
    pass


class ConnectionError(MapFileError):
    pass


class InvalidKeyError(MapFileError):
    pass


class MetadataError(MapFileError):
    pass


class InvalidLineError(MapFileError):
    pass


class InvalidDronesValue(MapFileError):
    pass
