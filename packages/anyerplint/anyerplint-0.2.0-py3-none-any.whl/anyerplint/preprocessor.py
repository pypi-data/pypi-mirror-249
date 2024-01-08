import re
from collections.abc import Iterable


def tokenize(cont: str) -> list[str]:
    return re.split(r"([{}\"])", cont)


def walk_tokens(toks: list[str]) -> Iterable[tuple[str, int]]:
    depth = 0
    in_string = False
    escaping = False
    acc = []
    current_start_line = 0
    lnum = 1
    for tok in toks:
        if not tok:
            # skip ''
            continue
        if depth > 0:
            acc.append(tok)
        match tok:
            case "{" if not in_string:
                depth += 1
                if depth == 1:
                    current_start_line = lnum
            case "}" if not in_string:
                depth -= 1
                if depth == 0:
                    # pop already pushed }
                    acc.pop()
                    yield ("".join(acc), current_start_line)
                    acc = []
            case '"' if not escaping and depth > 0:
                in_string = not in_string
            case _:
                ending_quote_count = len(tok) - len(tok.rstrip("\\"))
                escaping = ending_quote_count % 2 != 0

        lnum += tok.count("\n")


def get_expressions(cont: str) -> list[tuple[str, int]]:
    tokens = tokenize(cont)
    return list(walk_tokens(tokens))
