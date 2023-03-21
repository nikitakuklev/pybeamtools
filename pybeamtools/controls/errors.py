class ControlLibException(Exception):
    pass


class SecurityError(ControlLibException):
    pass


class InterlockWriteError(ControlLibException):
    pass


class InterlockTimeoutError(ControlLibException):
    pass


class InvalidWriteError(ControlLibException):
    pass


class WrappedException(Exception):
    ex: Exception
    tb: str
    pass
