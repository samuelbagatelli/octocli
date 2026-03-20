import re
from dataclasses import dataclass
from pathlib import Path

SQLTYPES: dict[str, str] = {
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
        sqltype: str | None = None,
        flags: ColumnFlags = ColumnFlags(),
    ) -> None:
        self.name = name
        self.pytype = pytype
        self.flags = flags

        self.sqltype = sqltype or SQLTYPES.get(pytype, pytype)

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

    def delete(self) -> None:
        if self.filepath.exists():
            self.filepath.unlink(True)

    def parsecols(self, src: str) -> list[dict]:
        cols: list[dict] = []

        pattern = re.compile(
            r"^\s{4}(\w+):\s*Mapped\[(.+?)\]\s*=\s*mapped_column\((.+?)\)",
            re.MULTILINE | re.DOTALL,
        )
        for attr in pattern.finditer(src):
            name, mtype, args = attr.group(1), attr.group(2), attr.group(3)
            optional = "Optional" in mtype
            rawtype = re.sub(r"Optional\[|\]", "", mtype).strip()

            nullable = "nullable=True" in args or "nullable=false" in args.lower()
            cols.append(
                {
                    "name": name,
                    "type": rawtype,
                    "optional": optional,
                    "nullable": nullable,
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

        for i, line in enumerate(lines):
            if re.match(r"^from\s+sqlalchemy", line):
                if newcol.sqltype not in line:
                    lines[i] = f"{line}, {newcol.sqltype}"
                break

        inclass = False
        insert_at = None
        last = None

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

    def rmcol(self, name: str) -> None:
        with self.filepath.open() as file:
            content = file.read()

        cols = self.parsecols(content)
        names = [col["name"] for col in cols]

        if name not in names:
            raise ValueError(f"Column '{name}' not found.")

        pattern = re.compile(
            rf"^\s{'{4}'}{re.escape(name)}:\s.+\([\s\S]*",
            re.MULTILINE,
        )
        match = pattern.findall(content)[0]

        lines = content.splitlines()
        lines.remove(match)

        finalstr = "\n".join(lines)
        with self.filepath.open("w") as file:
            file.write(finalstr)

    def list_columns(self) -> str:
        with self.filepath.open() as file:
            content = file.read()

        cols = self.parsecols(content)
        label = "\n  Style detected: modern (Mapped)"
        header = f"  {'Name':<20} {'Type':<15} {'Nullable':<10} {'Style'}"
        separator = "  " + "─" * 58
        lines: list[str] = []
        for col in cols:
            nullable = "✓" if col["nullable"] else "✗"
            line = f"  {col['name']:<20} {col['type']:<15} {nullable:<10} {'modern'}"
            lines.append(line)

        table = f"{label}\n{header}\n{separator}\n" + "\n".join(lines)

        return table
