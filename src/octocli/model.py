from pathlib import Path


class Model:
    def __init__(self, tablename: str) -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

    def create(self, destpath: Path = Path.cwd() / "models") -> None:
        temppath = Path(__file__).parent / "templates" / "models" / "standard.py"
        with temppath.open() as file:
            content = file.read()

        content = content.replace("{{ classname }}", self.classname)
        content = content.replace("{{ tablename }}", self.tablename)

        if not destpath.exists() and not destpath.name.endswith(".py"):
            destpath.mkdir()

        filepath = (
            destpath
            if destpath.name.endswith(".py")
            else Path(f"{destpath}/{self.tablename}.py")
        )
        with open(filepath, "w") as file:
            file.write(content)

    def read(self, srcpath: Path = Path.cwd() / "models") -> str:
        filepath = (
            srcpath
            if srcpath.name.endswith(".py")
            else Path(f"{srcpath}/{self.tablename}.py")
        )

        if not filepath.exists():
            return f"No such file or directory {filepath}"

        with open(filepath, "r") as file:
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
