import re
from pathlib import Path
from typing import TypedDict, Optional


class AddFlags(TypedDict):
    optional: bool
    nullable: bool


class Model:
    def __init__(self, tablename: str, dirpath: Path = Path.cwd() / "models") -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

        self.tmplpath = Path(__file__).parent / "templates" / "models" / "standard.py"

        if not dirpath.exists():
            dirpath.mkdir()

            initpath = dirpath / "__init__.py"
            initpath.touch()

        self.dirpath = dirpath
        self.filepath = self.dirpath / f"{self.tablename}.py"

    def create(self) -> None:
        with self.tmplpath.open() as file:
            content = file.read()

        content = content.replace("{{ classname }}", self.classname)
        content = content.replace("{{ tablename }}", self.tablename)

        with self.filepath.open("w") as file:
            file.write(content)

    def read(self) -> str:
        if not self.filepath.exists():
            return f"No such file or directory {self.filepath}"

        with self.filepath.open() as file:
            content = file.read()

        return content

    # def update(self, content: str) -> None:
    #     with self.filepath.open("w") as file:
    #         file.write(content)

    def delete(self) -> None:
        if self.filepath.exists():
            self.filepath.unlink(True)

    def parsecols(self, src: str) -> list:
        cols = []

        pattern = re.compile(
            r"^\s{4}(\w+):\s*Mapped\[(.+?)\]\s*=\s*mapped_column\((.+?)\)",
            re.MULTILINE | re.DOTALL,
        )
        for attr in pattern.finditer(src):
            name, mtype, args = attr.group(1), attr.group(2), attr.group(3)
            optional = "Optional" in mtype
            rawtype = re.sub(r"Optional\[|\]", "", mtype).strip()

            cols.append(
                {
                    "name": name,
                    "type": rawtype,
                    "optional": optional,
                    "raw": attr.group(0).strip(),
                    "args": args.strip(),
                }
            )

        return cols

    def addcol(self, name: str, pytype: str, flags: Optional[AddFlags] = None) -> None:
        with self.filepath.open() as file:
            content = file.read()

        self.parsecols(content)
