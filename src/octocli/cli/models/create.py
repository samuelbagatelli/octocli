from pathlib import Path
from typing import Annotated

from typer import Argument, Option, Typer

from ...core import OctoCliError


def model_create_factory(
    file_service: FileService,
    template_service: TemplateService,
    ui_service: UIService,
) -> Typer:
    app = Typer()

    @app.command()
    def create(
        tablename: Annotated[
            str,
            Argument(help="The incomplete (whitout prefix) table name."),
        ],
        is_duplicate: Annotated[
            bool,
            Option(
                help="Create a model only with id (no autoincrement) and created_at."
            ),
        ] = False,
    ) -> int:
        """Create a SQLAlchemy model file from template."""
        try:
            if not tablename.strip():
                ui_service.error("Table name cannot be empty.")
                return 1

            classname = tablename.title().replace("_", "")
            config = ModelConfig(
                tablename=tablename.strip(),
                classname=classname,
                is_duplicate=is_duplicate,
            )

            with ui_service.status("Creating model file..."):
                _create_model_file(config, file_service, template_service)

            ui_service.success(f"Model file created: models/{config.tablename}.py")
            return 0
        except OctoCliError as e:
            ui_service.error(str(e))
            return e.exit_code
        except Exception as e:
            ui_service.error(f"Unexpected error: {e}")
            return 1

    return app


def _create_model_file(
    config: ModelConfig,
    file_service: FileService,
    template_service: TemplateService,
) -> None:
    """Create a model file from configuration."""
    content = template_service.render_model_template(config)

    models_dir = Path.cwd() / "models"
    file_service.ensure_directory_exists(models_dir)

    file_path = models_dir / f"{config.tablename}.py"
    file_service.write_file(file_path, content)
