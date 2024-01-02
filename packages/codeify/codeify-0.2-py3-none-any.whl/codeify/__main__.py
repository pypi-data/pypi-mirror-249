from .codegen import run_generation
from .text import insert_text
from .types import CodeGeneration
from argparse import ArgumentParser
from typing import Callable
import sys
import traceback

def _parse_args() -> Callable[[], None]:
    parser = ArgumentParser(description='Codeify (code generator)') 
    subparsers = parser.add_subparsers(dest='command')

    _parse_insert_args(subparsers.add_parser('insert'))
    _parse_generate_args(subparsers.add_parser('generate'))

    args = parser.parse_args()
    if args.command == "generate":
        return lambda: run_generation(CodeGeneration(args.input, args.output, args.spec))
    elif args.command == "insert":
        return lambda: insert_text(args.input, args.text, args.before, args.after)
    else:
        parser.print_help()
        sys.exit(1)

def _parse_insert_args(parser: ArgumentParser) -> None:
    parser.add_argument('-i', '--input', help='input file', metavar='<file>', required=True)
    parser.add_argument('-B', '--before', help='text line before boundary', metavar='<str>')
    parser.add_argument('-A', '--after', help='text line after boundary', metavar='<str>')
    parser.add_argument('text', help='text to insert')

def _parse_generate_args(parser: ArgumentParser) -> None:
    parser.add_argument('-i', '--input', help='input directory', metavar='<dir>', required=True)
    parser.add_argument('-o', '--output', help='output directory', metavar='<dir>', required=True)
    parser.add_argument('-s', '--spec', help='specification file (yaml)', metavar='<spec.yaml>', required=True)

def main() -> int:
    try:
        _parse_args()()
        return 0
    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1
