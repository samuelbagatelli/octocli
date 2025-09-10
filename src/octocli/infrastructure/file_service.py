from pathlib import Path
from typing import Protocol


class FileService(Protocol):
    """Protocol for file operations."""

    def ensure_directory_exists(self, path: Path) -> None:
        """Ensure that a directory exists, creating it if necessary."""
        ...

    def write_file(self, path: Path, content: str) -> None:
        """Write content to a file."""
        ...


class LocalFileService:
    """Local filesystem implementation of FileService."""

    def ensure_directory_exists(self, path: Path) -> None:
        """Ensure that a directory exists, creating it if necessary."""
        try:
            path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise FileOperationError(f"Permission denied creating directory: {path}")
        except OSError as e:
            raise FileOperationError(f"Failed to create a directory {path}: {e}")

    def write_file(self, path: Path, content: str) -> None:
        """Write content to a file."""
        try:
            with path.open("w", encoding="utf-8") as file:
                file.write(content)
        except PermissionError:
            raise FileOperationError(f"Permission denied writing to file: {path}")
        except OSError as e:
            if e.errno == 28:
                raise FileOperationError(
                    f"Insufficient disk space to write file: {path}"
                )
            raise FileOperationError(f"Failed to write file {path}: {e}")
