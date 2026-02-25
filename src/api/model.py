import os


class Model:
    classname: str
    tablename: str

    def __init__(self, tablename: str) -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

    def create(self, dest: str = os.path.abspath(os.getcwd())) -> None:
        tpath = f"{dest}/templates/models/standard.py"
        with open(tpath) as file:
            content = file.read()

        content = content.replace("{{ classname }}", self.classname)
        content = content.replace("{{ tablename }}", self.tablename)

        dpath = f"{dest}/{self.tablename}.py"
        with open(dpath, "w") as file:
            file.write(content)

    def read(self, src: str = os.path.abspath(os.getcwd())) -> str:
        srcpath = src if src.endswith(".py") else f"{src}/{self.tablename}.py"
        with open(srcpath, "r") as file:
            content = file.read()

        return content

    def update(
        self,
        content: str,
        mode: str = "w",
        src: str = os.path.abspath(os.getcwd()),
    ) -> None:
        srcpath = src if src.endswith(".py") else f"{src}/{self.tablename}.py"
        with open(srcpath, mode) as file:
            file.write(content)

    def delete(self, src: str = os.path.abspath(os.getcwd())) -> None:
        srcpath = src if src.endswith(".py") else f"{src}/{self.tablename}.py"
        os.remove(srcpath)
