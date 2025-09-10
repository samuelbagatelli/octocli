from contextlib import contextmanager
from typing import Generator, Protocol

from rich.console import Console
from rich.status import Status


class UIService(Protocol):
    """Protocol for user interface operations."""

    def success(self, message: str) -> None:
        """Display a success message."""
        ...

    def error(self, message: str) -> None:
        """Display an error message."""
        ...

    def info(self, message: str) -> None:
        """Display an info message."""
        ...

    @contextmanager
    def status(self, message: str) -> Generator[Status, None, None]:
        """Display a status spinner with message."""
        ...


class RichUIService:
    """Rich-based UI service implementation."""

    def __init__(self, console: Console) -> None:
        self._console = console

    def success(self, message: str) -> None:
        """Display a success message."""
        self._console.print(f"[bold green]✓[/] {message}")

    def error(self, message: str) -> None:
        """Display an error message."""
        self._console.print(f"[bold red]✗ Error:[/] {message}")

    def info(self, message: str) -> None:
        """Display an info message."""
        self._console.print(f"[bold blue]ℹ[/] {message}")

    @contextmanager
    def status(self, message: str) -> Generator[Status, None, None]:
        """Display a status spinner with message."""
        with self._console.status(message, spinner="dots") as status:
            yield status
