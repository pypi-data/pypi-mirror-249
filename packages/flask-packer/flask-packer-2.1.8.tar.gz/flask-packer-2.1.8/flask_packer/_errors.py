class FlaskPackerException(Exception):
    """Base exception class."""

    pass


class NotInitialized(FlaskPackerException):
    """Raised when the extension has not been initialized."""

    pass


class FileTypeUnsupported(FlaskPackerException):
    """Raised when the file type is unsupported."""

    pass


class FileNotFound(FlaskPackerException):
    """Raised when a file could not be found."""

    pass
