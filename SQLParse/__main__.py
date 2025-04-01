import argparse
import os
import pdb

from localTypes import ProcessID
from SQLParser import SQLParser


def _define_args():
    """Define correctly the arguments needed by the program

    Returns
    -------
    argparse
        arguments parsed
    """
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
    return parser.parse_args()


def _handle_args(args):
    """Handle small exceptions related to input error

    Parameters
    ----------
    args : argparse
        parsed arguments to handle

    Returns
    -------
    tuple
        ``localTypes.ProcessID`` Enum and arguments of the program

    Raises
    ------
    NotImplementedError
        Not implemented yet
    NotImplementedError
        Not implemented yet
    NotImplementedError
        Not implemented yet
    SyntaxError
        Error in the syntax of the file given
    FileNotFoundError
        Input File is missing
    """
    if args.rst:
        process_id = ProcessID.RST
        raise NotImplementedError("restructured Text not supported yet")
    if args.md:
        process_id = ProcessID.MD
        raise NotImplementedError("Markdown not supported yet")
    if args.dblm:
        process_id = ProcessID.DBLM
    if args.filename:
        if os.path.isdir(args.filename):
            raise NotImplementedError("Folder processing not implemented yet")
        if not args.filename.endswith(".sql"):
            raise SyntaxError("The file provided does not ends as .sql")
        if not os.path.exists(args.filename):
            raise FileNotFoundError("File to process could not be found")
    return process_id, args


def main():
    """Main entrypoint of the CLI"""
    args = _define_args()
    process_id, definitive_args = _handle_args(args)
    if process_id is not None:
        print(SQLParser(definitive_args.filename))
    # pdb.set_trace()
    print("processing correctly")


if __name__ == "__main__":
    main()
