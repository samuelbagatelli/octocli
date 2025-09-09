from pathlib import Path
from typing import Annotated

from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from typer import Argument, Option, Typer

from ..errors import ErrorCode
from ..schemas import ModelConfig

app = Typer()
console = Console()


def create_file(config: ModelConfig) -> ErrorCode:
    env = Environment(
        loader=PackageLoader("octocli"),
        autoescape=select_autoescape(),
    )

    path = f"models/{'duplicate' if config.is_duplicate else 'standard'}.py.j2"
    template = env.get_template(path)

    buffer = template.render(config.model_dump())

    try:
        curr_dir = Path().cwd()
        models_dir = curr_dir / "models"

        console.print(f"Attempting to create directory: {models_dir}")
        models_dir.mkdir()
        console.print("New directory '/models' created.")
    except FileExistsError:
        pass
    except Exception as e:
        console.print("[bold red]Unexpected error occured[/]")
        console.print(e)
        return ErrorCode.UNKNOWN_ERROR

    with open(f"models/{config.tablename}.py", "w") as file:
        file.write(buffer)

    return ErrorCode.SUCCESS


@app.command()
def create(
    tablename: Annotated[
        str,
        Argument(help="The incomplete (whithout prefix) table name."),
    ],
    is_duplicate: Annotated[
        bool,
        Option(help="Create a duplicate table model representation."),
    ] = False,
) -> ErrorCode:
    classname = tablename.title().replace("_", "")

    config = ModelConfig(
        tablename=tablename,
        classname=classname,
        is_duplicate=is_duplicate,
    )

    err_code = create_file(config)

    return err_code
