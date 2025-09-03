from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from typer import Typer

app = Typer()
console = Console()


def create_duplicate(environment: Environment) -> None:
    path = "models/duplicate.py.j2"
    template = environment.get_template(path)


def create_standard(environment: Environment) -> None:
    path = "models/standard.py.j2"
    template = environment.get_template(path)


@app.command()
def create(model_name: str, is_duplicate: bool = False) -> None:
    class_name = model_name.title()

    environ = Environment(
        loader=PackageLoader("octocli"),
        autoescape=select_autoescape(),
    )
    create_duplicate(environ) if is_duplicate else create_standard(environ)
