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


class MapFileError(Exception):
    def __init__(self, line, message):
        self.line = line
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        error = bcolors.FAIL + "[MapFileError]" + bcolors.ENDC
        return error + f" Line {self.line}: {self.message}"


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
