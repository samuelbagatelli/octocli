import os
import tomllib

from rich import print
from typer import Exit, Option, Typer

app = Typer(name="octocli")


def version_callback(v: bool) -> None:
    if v:
        path = os.getcwd()
        with open(f"{path}/pyproject.toml", "rb") as file:
            data = tomllib.load(file)
            version = data.get("project", {"version": "0.1.0"}).get("version")
            print(f"OctoCLI {version}")
        raise Exit()


@app.callback()
def commom(
    version: bool = Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
    )
) -> None:
    pass


if __name__ == "__main__":
    app()
