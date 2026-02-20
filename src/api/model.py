import os


class Model:
    classname: str
    tablename: str

    def __init__(self, tablename: str) -> None:
        self.tablename = tablename
        self.classname = tablename.title().replace("_", "")

    def create(self, dest: str = os.path.abspath(os.getcwd())) -> None:
        # reads the template
        tpath = f"{dest}/templates/models/standard.py"
        with open(tpath) as file:
            content = file.read()

        content = content.replace("{{ classname }}", self.classname)
        content = content.replace("{{ tablename }}", self.tablename)

        # create file in `dest` directory
        dpath = f"{dest}/{self.tablename}.py"
        with open(dpath, "w") as file:
            file.write(content)

    def read(self) -> None:
        pass

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass


m = Model("table_name")

m.create()
