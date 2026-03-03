import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SQLTYPES = {
    "str": "String",
    "int": "Integer",
    "float": "Float",
    "bool": "Boolean",
    "datetime": "DateTime",
    "date": "Date",
    "bytes": "LargeBinary",
    "dict": "JSON",
    "list": "JSON",
}


@dataclass
class ColumnFlags:
    nullable: bool = False
    primary_key: bool = False
    unique: bool = False
    index: bool = False
    autoincrement: bool = False


class Column:
    def __init__(
        self,
        name: str,
        pytype: str,
        sqltype: Optional[str] = None,
        flags: ColumnFlags = ColumnFlags(),
    ) -> None:
        self.name = name
        self.pytype = pytype
        self.flags = flags

        self.sqltype = sqltype or SQLTYPES[pytype]

    def build(self, indent: str = "    ") -> str:
        mapped = f"Optional[{self.pytype}]" if self.flags.nullable else self.pytype

        args = [self.sqltype]
        args.append(f"nullable={self.flags.nullable}")

        if self.flags.primary_key:
            args.append("primary_key=True")
        if self.flags.unique:
            args.append("unique=True")
        if self.flags.index:
            args.append("index=True")
        if self.flags.autoincrement:
            args.append("autoincrement=True")

        attrcolstr = f"{indent}{self.name}: Mapped[{mapped}] = mapped_column("

        if len(args) > 2:
            for i, arg in enumerate(args):
                args[i] = f"\n{indent * 2}{arg}"

            strargs = ",".join(args)

            attrcolstr += strargs
            attrcolstr += f"\n{indent})"
        else:
            strargs = ", ".join(args)
            attrcolstr += f"{strargs})"

        return attrcolstr


class Model:
    def __init__(self, tablename: str, dirpath: Path = Path.cwd() / "models") -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

        if not dirpath.exists():
            dirpath.mkdir()

            initpath = dirpath / "__init__.py"
            initpath.touch()

        self.dirpath = dirpath
        self.filepath = self.dirpath / f"{self.tablename}.py"

    def create(self) -> None:
        template_path = Path(__file__).parent / "templates" / "models" / "standard.py"
        with template_path.open() as file:
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

    def addcol(
        self,
        name: str,
        pytype: str,
        flags: ColumnFlags = ColumnFlags(),
    ) -> None:
        with self.filepath.open() as file:
            content = file.read()

        cols = self.parsecols(content)
        if any(col["name"] == name for col in cols):
            raise ValueError(f"Column '{name}' already in model '{self.tablename}'.")

        newcol = Column(name, pytype, flags=flags)
        colstr = newcol.build()

        lines = content.splitlines()

        # insert sqlalchemy type import
        for i, line in enumerate(lines):
            if re.match(r"^from\s+sqlalchemy", line):
                if newcol.sqltype not in line:
                    lines[i] = f"{line}, {newcol.sqltype}"
                break

        inclass = False
        insert_at = None
        last = None

        # find line to insert at
        for i, line in enumerate(lines):
            if re.match(r"^class\s+\w+", line):
                inclass = True
            if inclass:
                if re.match(r"^\s{4}(def |@)", line):
                    insert_at = i
                    break
                if re.match(r"^s{4}\w+", line) and ("=" in line or ":" in line):
                    last = i

        if insert_at is None:
            insert_at = (last + 1) if last is not None else len(lines)

        lines.insert(insert_at, colstr)

        with self.filepath.open("w") as file:
            file.write("\n".join(lines))
