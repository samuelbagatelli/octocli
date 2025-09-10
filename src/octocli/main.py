from rich.console import Console
from typer import Typer

from octocli.infrastructure.file_service import LocalFileService
from octocli.infrastructure.template_service import Jinja2TemplateService
from octocli.presentation.ui import RichUIService

from .cli.models import create_model_factory


def create_app() -> Typer:
    """Create the main application with all dependencies wired up."""
    console = Console()
    file_service = LocalFileService()
    template_service = Jinja2TemplateService()
    ui_service = RichUIService(console)

    app = Typer(
        name="octocli",
        help="Generate SQLAlchemy model files from Jinja2 templates",
        add_completion=False,
    )

    create_app_instance = create_model_factory(
        file_service=file_service,
        template_service=template_service,
        ui_service=ui_service,
    )

    app.add_typer(create_app_instance, name="create")

    return app


if __name__ == "__main__":
    app = create_app()
    app()
