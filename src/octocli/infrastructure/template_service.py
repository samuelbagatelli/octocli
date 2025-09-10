from typing import Protocol

from jinja2 import Environment, PackageLoader, TemplateError, select_autoescape


class TemplateService(Protocol):
    """Protocol for template rendering services."""

    def render_model_template(self, config: ModelConfig) -> str:
        """Render a model template with the given configuration."""
        ...


class Jinja2TemplateService:
    """Jinja2-based template rendering service."""

    def __init__(self, package_name: str = "octocli") -> None:
        """Initialize the Jinja2 environment."""
        try:
            self._env = Environment(
                loader=PackageLoader(package_name),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
        except Exception as e:
            raise TemplateError(f"Failed to initialize template environment: {e}")

    def render_model_template(self, config: ModelConfig) -> str:
        """Render a model template with the given configuration."""
        try:
            template_path = (
                f"models/{'duplicate' if config.is_duplicate else 'standard'}.py.j2"
            )
            template = self._env.get_template(template_path)
            return template.render(config.model_dump())
        except Exception as e:
            raise TemplateError(f"Failed to render template: {e}")
