from pathlib import Path


class Model:
    def __init__(self, tablename: str) -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

    def create(self, destpath: Path = Path.cwd() / "models") -> None:
        tmplpath = Path(__file__).parent / "templates" / "models" / "standard.py"
        with tmplpath.open() as file:
            content = file.read()

        content = content.replace("{{ classname }}", self.classname)
        content = content.replace("{{ tablename }}", self.tablename)

        ispyfile = destpath.name.endswith(".py")
        if not destpath.exists() and not ispyfile:
            destpath.mkdir()

        filepath = destpath if ispyfile else destpath / f"{self.tablename}.py"
        with filepath.open("w") as file:
            file.write(content)

    def read(self, srcpath: Path = Path.cwd() / "models") -> str:
        filepath = (
            srcpath
            if srcpath.name.endswith(".py")
            else Path(f"{srcpath}/{self.tablename}.py")
        )

        if not filepath.exists():
            return f"No such file or directory {filepath}"

        with filepath.open("r") as file:
            content = file.read()

        return content

    def update(self, content: str, srcpath: Path = Path.cwd() / "models") -> None:
        filepath = (
            srcpath
            if srcpath.name.endswith(".py")
            else Path(f"{srcpath}/{self.tablename}.py")
        )
        with filepath.open("w") as file:
            file.write(content)

    def delete(self, srcpath: Path = Path.cwd() / "models") -> None:
        filepath = (
            srcpath
            if srcpath.name.endswith(".py")
            else Path(f"{srcpath}/{self.tablename}.py")
        )
        if filepath.exists():
            filepath.unlink(True)
