from argparse import ArgumentParser, RawDescriptionHelpFormatter

from octocli import __version__
from octocli.model import Model


def build_parser() -> ArgumentParser:
    parser = ArgumentParser("octo", formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"🐙 OctoCLI {__version__} 🐙",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "init",
        help="Initialize a FastAPI repository on CPID patterns",
    )

    model_parser = subparsers.add_parser(
        "model",
        help="Manages SQLAlchemy Models on cwd",
    )
    model_subparser = model_parser.add_subparsers(dest="action", required=True)

    model_create = model_subparser.add_parser(
        "create",
        help="Create a model following CPID standard pattern",
    )
    model_create.add_argument("tablename", required=True, help="SQL table name")

    model_read = model_subparser.add_parser(
        "read",
        help="Prints the file content on stdout",
    )
    model_read.add_argument("tablename", required=True, help="SQL table name")

    model_delete = model_subparser.add_parser(
        "delete",
        help="Deletes Model file of the provided tablename",
    )
    model_delete.add_argument("tablename", required=True, help="SQL table name")

    model_list = model_subparser.add_parser(
        "list",
        help="List columns of tablename on a table view",
    )
    model_list.add_argument("tablename", required=True, help="SQL table name")

    model_addcol = model_subparser.add_parser(
        "add",
        help="Add a column/attribute on a Model with tablename",
    )
    model_addcol.add_argument("tablename", required=True, help="SQL table name")
    model_addcol.add_argument("--name", help="Name of the column")
    model_addcol.add_argument("--type", help="Python type of the column")

    model_rmcol = model_subparser.add_parser(
        "remove",
        help="Remove a column/attribute on a Model with tablename",
    )
    model_rmcol.add_argument("tablename", required=True, help="SQL table name")
    model_rmcol.add_argument("--name", help="Name of the column")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        print("Not implemented yet")
    elif args.command == "model":
        model = Model(args.tablename)
        match args.action:
            case "create":
                model.create()
            case "read":
                print(model.read())
            case "delete":
                model.delete()
            case "add":
                model.addcol(args.name, args.type)
            case "remove":
                model.rmcol(args.name)


if __name__ == "__main__":
    main()
