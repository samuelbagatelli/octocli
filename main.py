from src.octocli.model import Model

m = Model("user")

while True:
    char = input()
    match char:
        case "C" | "c":
            m.create()
        case "R" | "r":
            print(m.read())
        # case "U" | "u":
        #     m.update("test")
        case "D" | "d":
            m.delete()
        case "A" | "a":
            colname = input("insert column name: ")
            pytype = input("insert python type of the column: ")

            m.addcol(colname, pytype)
        case "q":
            break
        case _:
            pass
