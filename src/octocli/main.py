from rich import print
from typer import Typer

app = Typer(name="octocli")


@app.command()
def load():
    print("Loading portal gun")
