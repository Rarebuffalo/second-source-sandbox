"""Command-line interface: ``python -m textkit <command> <text> [options]``.

Each public function is a command that prints its result. A usage error, such as an unknown
command, exits with status 2 and a short usage message (argparse's convention).
"""

import argparse
import sys

from textkit.core import slugify, title_case, truncate, word_count


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m textkit", description="Tiny text utilities.")
    commands = parser.add_subparsers(dest="command", required=True, metavar="command")

    for name, func in (("slugify", slugify), ("word_count", word_count), ("title_case", title_case)):
        sub = commands.add_parser(name, help=func.__doc__.splitlines()[0])
        sub.add_argument("text")

    sub = commands.add_parser("truncate", help=truncate.__doc__.splitlines()[0])
    sub.add_argument("text")
    sub.add_argument("limit", type=int)
    sub.add_argument("--suffix", default="...")
    sub.add_argument("--whole-words", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "slugify":
        result = slugify(args.text)
    elif args.command == "word_count":
        result = word_count(args.text)
    elif args.command == "title_case":
        result = title_case(args.text)
    else:
        try:
            result = truncate(args.text, args.limit, args.suffix, whole_words=args.whole_words)
        except ValueError as exc:
            parser.error(str(exc))
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
