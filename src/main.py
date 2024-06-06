"""
Darknet Diaries Podcast Download Tool.
For those that love the show but not the cumbersome podcast apps.

#     a = tree.xpath("//*[name()='itunes:title']")

https://realpython.com/command-line-interfaces-python-argparse/

"""

import argparse

from pathlib import Path

from importlib.resources import files


def load_data() -> str:
    """This function loads the xml page saved as a package resource."""
    return files('mypkg').joinpath('dn_page.xml').read_text()


def fn(*args) -> None:
    print('fn')


def fn1(*args) -> None:
    print('fn1')


def fn2(*args) -> None:
    print('fn2')


def fn3(*args) -> None:
    print('fn3')


def fn4(*args) -> None:
    print('fn4')


def fn5(*args) -> None:
    print('fn5')


def fn6(*args) -> None:
    print('fn6')


def main():
    """Commandline interface for Darknet Diaries Podcast Download Tool.
    """

    parser = argparse.ArgumentParser(
        prog="darknetdiaries",
        description='Darknet Diaries Podcast Download Tool.',
        epilog="""Don't forget to support the show by donating
        at https://darknetdiaries.com/donate/""")

    parser.add_argument("path",
                        default=".",
                        help="Destination download folder.")

    general = parser.add_argument_group("General Output")

    general.add_argument("-v", "--verbose", action="store_true")
    general.add_argument("-s", "--silent", action="store_true")
    general.add_argument("-r", "--random", action="store_true")

    subparsers = parser.add_subparsers(title="Options", metavar='')

    arg_template = {
        "dest": "operands",
        "type": int,
        "nargs": "*",
        "metavar": "OPERAND",
        "help": "A list of tracks when relevant.",
    }
    all_parser = subparsers.add_parser("all",
                                       help='Download all the episodes.')
    all_parser.add_argument(**arg_template)
    all_parser.set_defaults(func=fn)

    multiple_parser = subparsers.add_parser("multiple",
                                            help='Download a list of episodes')
    multiple_parser.add_argument(**arg_template)
    multiple_parser.set_defaults(func=fn1)

    single_parser = subparsers.add_parser("single",
                                          help='Download a single episodes.')
    single_parser.add_argument(**arg_template)
    single_parser.set_defaults(func=fn2)

    list_parser = subparsers.add_parser("list",
                                        help='List all the  episodes by name.')
    list_parser.add_argument(**arg_template)
    list_parser.set_defaults(func=fn5)

    detail_parser = subparsers.add_parser(
        "detail",
        help='Show episode details for a list of 1 or more episodes.')
    detail_parser.add_argument(**arg_template)
    detail_parser.set_defaults(func=fn6)

    args = parser.parse_args()

    dest_folder = Path(args.path)
    if not dest_folder.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)
    print(args)
    print(*args.operands)
    args.func(*args.operands)


if __name__ == '__main__':
    main()
