class OctoCliError(Exception):
    """Base exception for OctoCLI errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class TemplateError(OctoCliError):
    """Exception raised for template-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Template error: {message}", exit_code=2)


class FileOperationError(OctoCliError):
    """Exception raised for file operation errors."""

    def __init__(self, message: str) -> None:
        super().__init__(f"File operation error: {message}", exit_code=3)
