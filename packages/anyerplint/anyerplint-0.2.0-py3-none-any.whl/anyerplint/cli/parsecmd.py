import argparse
import sys

from rich.console import Console

from anyerplint.preprocessor import get_expressions
from anyerplint.recursive_list import RecursiveList
from anyerplint.tnex import Translator, parse
from anyerplint.util import glob_plus, open_text_file

console = Console(highlight=False)


def emit(s: str) -> None:
    console.print(s)


def color(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


def print_recursive_lists(tree: RecursiveList[str], indent: int) -> None:
    first = True
    for el in tree:
        if isinstance(el, list):
            print_recursive_lists(el, indent + 1)
        else:
            if first:
                col = "deep_sky_blue1"
            elif el.startswith('"') and el.endswith('"'):
                col = "dark_orange"
            elif el.lower().startswith("v,"):
                col = "bright_green"
            elif el.isdecimal():
                col = "bright_yellow"
            else:
                col = None

            t = color(el, col) if col else el
            emit("  " * (indent + (not first)) + t)
            first = False


def color_translation_errors(expr: str) -> str:
    return expr.replace("~(~", "[red]").replace("~)~", "[/red]")


def print_formatted_expression(
    exp: str, linenum: int, errors_only: bool, log_all: bool
) -> None:
    try:
        parsed = parse(exp)
        translator = Translator()
        translated = translator.translate(parsed[0])
    except ValueError:
        emit("[red]Failed to parse[/]: " + exp)
        return

    if errors_only and not translator.errors:
        return

    non_trivial_expr = translated != exp
    if non_trivial_expr or log_all:
        emit(f"L[yellow]{linenum}[/]\t[grey66]{exp}[/]")
    if non_trivial_expr:
        emit("=>\t" + color_translation_errors(translated))
        expr = parsed[0]
        if not isinstance(expr, list):
            return
        print_recursive_lists(expr, 1)
        emit("")


def print_all_expressions(cont: str, errors_only: bool, log_all: bool) -> None:
    expressions = get_expressions(cont)

    for exp, linenum in expressions:
        print_formatted_expression(exp, linenum, errors_only, log_all)


def handle_parse(args: argparse.Namespace) -> None:
    errors_only = args.errors
    console.no_color = args.no_color
    if not args.filename:
        console.rule("stdin")
        cont = sys.stdin.read()
        print_all_expressions(cont, errors_only, log_all=True)

    for pat in args.filename:
        fnames = glob_plus(pat)
        for f in fnames:
            console.rule(str(f))
            cont = open_text_file(f).read()
            print_all_expressions(cont, errors_only, log_all=False)


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.add_argument("filename", nargs="*", help="Files to parse")
    parser.add_argument(
        "--errors", action="store_true", help="Print only expressions with errors"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="No colors, good for redirecting to file",
    )
    parser.set_defaults(func=handle_parse)
    return parser
