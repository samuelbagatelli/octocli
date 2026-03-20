from argparse import ArgumentParser, RawDescriptionHelpFormatter

from octocli import __version__
from octocli.model import Model


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        "octo",
        formatter_class=RawDescriptionHelpFormatter,
        description="OctoCLI - Manage FastAPI/SQLAlchemy backend applications",
    )

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
        help="Manage SQLAlchemy models",
    )
    model_subparser = model_parser.add_subparsers(dest="model_action", required=True)

    model_add = model_subparser.add_parser("add", help="Create a new model")
    model_add.add_argument("tablename", help="SQL table name")

    model_rm = model_subparser.add_parser("rm", help="Delete a model")
    model_rm.add_argument("tablename", help="SQL table name")

    model_show = model_subparser.add_parser("show", help="Show model file contents")
    model_show.add_argument("tablename", help="SQL table name")

    model_ls = model_subparser.add_parser("ls", help="List model columns")
    model_ls.add_argument("tablename", help="SQL table name")

    column_parser = subparsers.add_parser(
        "column",
        help="Manage model columns",
    )
    column_subparser = column_parser.add_subparsers(dest="column_action", required=True)

    column_add = column_subparser.add_parser("add", help="Add a column to a model")
    column_add.add_argument("tablename", help="SQL table name")
    column_add.add_argument("column", help="Column name")
    column_add.add_argument("--type", required=True, help="Python type of the column")

    column_rm = column_subparser.add_parser("rm", help="Remove a column from a model")
    column_rm.add_argument("tablename", help="SQL table name")
    column_rm.add_argument("column", help="Column name")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        print("Not implemented yet")
    elif args.command == "model":
        model = Model(args.tablename)
        if args.model_action == "add":
            model.create()
        elif args.model_action == "rm":
            model.delete()
        elif args.model_action == "show":
            print(model.read())
        elif args.model_action == "ls":
            print(model.list_columns())
    elif args.command == "column":
        model = Model(args.tablename)
        if args.column_action == "add":
            model.addcol(args.column, args.type)
        elif args.column_action == "rm":
            model.rmcol(args.column)


if __name__ == "__main__":
    main()
