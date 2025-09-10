from dataclasses import dataclass
from typing import Protocol

from rich.console import Console

from octocli.infrastructure.file_service import FileService, LocalFileService
from octocli.infrastructure.template_service import (Jinja2TemplateService,
                                                     TemplateService)
from octocli.presentation.ui import RichUIService, UIService


class DependencyContainer(Protocol):
    """Protocol for dependency containers."""

    console: Console
    file_service: FileService
    template_service: TemplateService
    ui_service: UIService


@dataclass
class Dependencies:
    """Container for all application dependencies."""

    console: Console
    file_service: FileService
    template_service: TemplateService
    ui_service: UIService

    @classmethod
    def create_production(cls) -> "Dependencies":
        """Create production dependencies."""
        console = Console()
        file_service = LocalFileService()
        template_service = Jinja2TemplateService()
        ui_service = RichUIService(console)

        return cls(
            console=console,
            file_service=file_service,
            template_service=template_service,
            ui_service=ui_service,
        )
