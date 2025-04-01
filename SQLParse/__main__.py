import argparse
import os


def _define_args():
    parser = argparse.ArgumentParser(
        prog="SQLParse",
        description="Parse SQL and generate Documentation",
        epilog="Work in progress",
    )
    parser.add_argument("filename")  # positional argument
    parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--rst",
        help="rst export flag",
        action="store_true",
    )
    group.add_argument("--md", help="markdown export flag", action="store_true")
    group.add_argument("--dblm", help="DBLM export flag", action="store_true")
    parser.print_help()
    return parser.parse_args()


def _handle_args(args):
    if args.rst:
        raise NotImplementedError("restructured Text not supported yet")
    if args.md:
        raise NotImplementedError("Markdown not supported yet")
    if args.dblm:
        process_id = 3
    if args.filename:
        if os.path.isdir(args.filename):
            raise NotImplementedError("Folder processing not implemented yet")
        if not args.filename.endswith(".sql"):
            raise SyntaxError("The file provided does not ends as .sql")
        if not os.path.exists(args.filename):
            raise FileNotFoundError("File to process could not be found")
    return process_id, args


def main():
    args = _define_args()
    process_id, definitive_args = _handle_args(args)
    print("processing correctly")


if __name__ == "__main__":
    main()
