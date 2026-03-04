from pathlib import Path
import sys
from octocli import __version__

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from octocli.model import ColumnFlags, Model


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="octo",
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""
exemplos:
    octo models                         # modo interativo
    octo models user read            # ler arquivo
    octo models user add phone str   # adicionar coluna
    octo models user add age int --nullable --default=0
    octo models user add token str --nullable
    octo models user rm phone        # remover coluna
        """,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"octo {__version__}",
    )

    parser.add_argument("directory", help="Caminho para o diretório")

    parser.add_argument("tablename", nargs="?", help="Nome da tabela/model")

    subparsers = parser.add_subparsers(dest="action", help="Ações disponíveis")

    parser_list = subparsers.add_parser("list", help="List columns of model")

    parser_read = subparsers.add_parser("read", help="Ler o conteúdo do arquivo")

    parser_add = subparsers.add_parser("add", help="Adicionar uma nova coluna")
    parser_add.add_argument("column", help="Nome da coluna/atributo")
    parser_add.add_argument("type", help="Tipo de dado (ex: str, int)")
    parser_add.add_argument(
        "--nullable",
        action="store_true",
        help="Define se a coluna pode ser nula",
    )
    parser_add.add_argument("--default", type=str, help="Valor padrão da coluna")

    parser_rm = subparsers.add_parser("rm", help="Remover coluna existente")
    parser_rm.add_argument("column", help="Nome da coluna/atributo a ser removida(o)")

    subparsers.add_parser("interactive", aliases=["i"], help="Modo interativo com menu")

    return parser


def _interactive(model: Model) -> None:
    print(f"\n  ╔══════════════════════════════╗")
    print(f"  ║   fam — FastAPI Model Mgr    ║")
    print(f"  ╚══════════════════════════════╝")
    print(f"  Arquivo : {model.filepath}")

    while True:
        print("  [1] Ler conteúdo arquivo")
        print("  [2] Adicionar coluna")
        print("  [3] Remover coluna")
        print("  [4] Listar colunas")
        print("  [0] Sair\n")
        choice = input("  > ").strip()

        if choice == "0":
            print("  Saindo.\n")
            break
        elif choice == "1":
            print(model.read())
        elif choice == "2":
            print()
            name = input("  Nome da coluna               : ").strip()
            py_type = input("  Tipo Python (padrão: str)    : ").strip() or "str"
            nullable = input("  Nullable no banco? [s/N]     : ").strip().lower() == "s"
            pk = input("  Primary key? [s/N]           : ").strip().lower() == "s"
            unique = input("  Unique? [s/N]           : ").strip().lower() == "s"
            index = input("  Index? [s/N]           : ").strip().lower() == "s"
            autoincrement = (
                input("  Autoincrement? [s/N]           : ").strip().lower() == "s"
            )
            print()
            try:
                flags = ColumnFlags(
                    nullable=nullable,
                    primary_key=pk,
                    unique=unique,
                    index=index,
                    autoincrement=autoincrement,
                )
                model.addcol(name, py_type, flags)
                print(f"  ✓ Coluna '{name}: {py_type}' adicionada com sucesso!\n")
            except Exception as e:
                print(f"  ✗ Erro: {e}\n")
        elif choice == "3":
            name = input("  Nome da coluna a remover: ").strip()
            confirm = input(f"  Confirmar remoção de '{name}'? [s/N]: ").strip().lower()
            if confirm == "s":
                try:
                    model.rmcol(name)
                    print(f"\n  ✓ Coluna '{name}' removida com sucesso.\n")
                except Exception as e:
                    print(f"\n  ✗ Erro: {e}\n")
            else:
                print("  Operação cancelada")
        elif choice == "4":
            print(model.lscols())
        else:
            print("  Opção inválida.\n")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dirpath = Path(args.directory)
    tablename = args.tablename

    model = Model(tablename, dirpath)
    model.create()

    if args.action in (None, "interactive", "i"):
        _interactive(model)
    elif args.action == "list":
        try:
            print(model.lscols())
        except Exception as e:
            print(f"octo: erro: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.action == "read":
        try:
            print(model.read())
        except Exception as e:
            print(f"octo: erro: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.action == "add":
        try:
            flags = ColumnFlags(
                nullable=args.nullable,
                primary_key=args.primary_key,
                unique=args.unique,
                index=args.index,
                autoincrement=args.autoincrement,
            )
            model.addcol(args.name, args.type, flags)
            print(
                f"✓ Coluna '{args.name}: {args.type}' adicionada em '{model.filepath}'"
            )
        except Exception as e:
            print(f"octo: erro: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.action == "remove":
        try:
            model.rmcol(args.name)
            print(f"✓ Coluna '{args.name}' removida de '{model.filepath}'")
        except Exception as e:
            print(f"octo: erro: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
