"""tnex - Trivial Nested EXpressions.

Easier to read/write than s-expr's I guess

"""
import re

from anyerplint import util
from anyerplint.recursive_list import RecursiveList


def tokenize(s: str) -> list[str]:
    # negative lookbehind for \ escaping, split to parts separated by ; ( ) "
    tokens = re.split(r"([\(\)\";])", s)
    return list(filter(None, tokens))


class ParseError(Exception):
    """Exceptions raised by parser."""


def _parse_string(toks: list[str]) -> tuple[str, int]:
    assert toks[0] == '"'
    # eat up tokens to produce just one str
    result = ['"']
    escape = False
    for tok in util.skip(toks, 1):
        result.append(tok)
        if tok.endswith("\\"):
            backslashes = len(tok) - len(tok.rstrip("\\"))
            escape = (backslashes % 2) != 0
        elif tok == '"' and not escape:
            value = "".join(result)
            return value, len(result)
        else:
            escape = False

    msg = "Unterminated string"
    raise ParseError(msg)


def _parse_accessor(toks: list[str]) -> tuple[str, int]:
    if len(toks) > 1 and toks[1] == '"':
        s, moved = _parse_string(toks[1:])
        return toks[0] + s, moved + 1

    return toks[0], 1


def emit_nested_sequence(parts: list[str]) -> tuple[RecursiveList[str], int]:
    res: RecursiveList[str] = []
    i = 0
    while i < len(parts):
        it = parts[i]
        if it == '"':
            s, moved = _parse_string(parts[i:])
            res.append(s)
            i += moved
        elif it == ";":
            i += 1
        elif it == ")":
            i += 1
            break
        elif it == "(":
            nested, moved = emit_nested_sequence(parts[i + 1 :])
            nested.insert(0, parts[i - 1].strip())
            res = res[0:-1]
            res.append(nested)
            i += moved
        elif it.startswith(","):
            # actually call previous output with "nesting" output
            previous = res.pop()
            s, moved = _parse_accessor(parts[i:])
            res.append([s, previous])
            i += moved

        # special foo,"hello" accessor that accesses property of foo.
        # lexer breaks it because of " char, so reassemble it here
        elif it.endswith(","):
            s, moved = _parse_accessor(parts[i:])
            res.append(s)
            i += moved
        else:
            res.append(it)
            i += 1

    return (res, i + 1)


def removequote(s: str) -> str:
    return s.removeprefix('"').removesuffix('"')


def translate_str(s: str) -> str | list[str]:
    parsed = parse(s)
    translator = Translator()
    result = translator.translate(parsed[0])
    errors = translator.errors
    return errors if errors else result


# these will be converted to uppercase variants. Eventually this should be empty but needs fixing a lot of templates

allow_wrong_case = {
    "F,Calc",
    "F,Combine",
    "F,Eval",
    "F,IsChanged",
    "F,Not",
    "F,SetData",
    "F,ToDate",
}

# some 'trivial' translations
nullary_funcs = {
    "F,GUID",
    "F,NOW",
}
# these will be translated to name(arg1; arg2)
# xxx remove the mixed case variants
nnary_funcs: dict[str, int | tuple[int, int]] = {
    "F,ADDXMLNS": 4,
    "F,CSV": (2, 3),
    "F,DATEADD": 3,
    "F,DATEDIFF": 3,
    "F,DBSELECT": (2, 999),
    "F,FLOOR": 1,
    "F,ISCHANGED": 2,
    "F,ISDATE": (1, 2),
    "F,ISNOTHING": 0,
    "F,ISNUMERIC": 1,
    "F,LPAD": 3,
    "F,PARSE": 1,
    "F,RANGE": 4,
    "F,ROUND": (2, 3),
    "F,RPAD": 3,
    "F,SAPSELECT": 6,
    "F,XMLENCODE": 1,
}


class Translator:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def translate(self, tree: str | RecursiveList[str]) -> str:
        """Convert to pretty mostly-infix notation."""
        # only lists cause translation
        if not isinstance(tree, list):
            return str(tree)

        translate = self.translate
        func_name = tree[0]
        if isinstance(func_name, str) and func_name in allow_wrong_case:
            tree[0] = func_name.upper()
        match tree:
            case ["F,EVAL", obj, operation, comp, iftrue, iffalse]:
                return f"({translate(obj)} {removequote(translate(operation))} {translate(comp)} ? {translate(iftrue)} : {translate(iffalse)})"
            case ["F,EXISTS", "v", key]:
                return f"defined({key})"
            case ["F,EXISTS", obj, key]:
                return f"({key} in {translate(obj)})"
            case ["F,EXISTS", obj]:
                return f"(exists {translate(obj)})"

            case ["F,REPLACE", src, frome, toe]:
                return (
                    f"{translate(src)}.replace({translate(frome)} -> {translate(toe)})"
                )
            case ["F,LOWER", exp]:
                return f"{translate(exp)}.lower()"
            case ["F,UPPER", exp]:
                return f"{translate(exp)}.upper()"
            case ["F,TRIM", exp]:
                return f"{translate(exp)}.trim()"
            case ["F,LTRIM", exp]:
                return f"{translate(exp)}.ltrim()"
            case ["F,RTRIM", exp]:
                return f"{translate(exp)}.rtrim()"

            case ["F,NVL", exp, default]:
                return "(" + translate(exp) + " ?? " + translate(default) + ")"

            case ["F,TONUMBER", exp, '"."']:
                return f"num({translate(exp)})"
            case ["F,TONUMBER", exp, sep]:
                return f"num({translate(exp)} - {translate(sep)})"
            case ["F,TOCHAR", exp, str(format)]:
                return f"num({translate(exp)}.tochar({format})"
            case ["F,TOCHAR", exp, str(format), str(culture)]:
                return f"num({translate(exp)}.tochar({format}, {culture})"
            case ["F,FORMAT", exp, format]:
                return f"{translate(exp)}.format({translate(format)})"
            case ["F,COMBINE", *parts]:
                translated = [translate(part) for part in parts]
                return "(" + " & ".join(translated) + ")"
            case ["F,GETDATA", ds, key]:
                return f"{translate(ds)}[{translate(key)}]"
            case ["F,GETNODE", src, path]:
                return f"{translate(src)}.node({translate(path)})"
            case ["F,SETDATA", ds, key, value]:
                return f"{translate(ds)}[{translate(key)}] := {translate(value)}"
            case ["F,IF", src, op, tgt]:
                return (
                    f"if {translate(src)} {removequote(translate(op))} {translate(tgt)}"
                )
            case ["F,LEN", o]:
                return f"len({translate(o)})"
            case ["F,CALC", *parts]:
                return "(" + " ".join(translate(part) for part in parts) + ")"
            case ["F,NOT", exp]:
                return "not " + translate(exp)
            case ["F,AND", *conds]:
                translated = [translate(part) for part in conds]
                return "(" + " && ".join(translated) + ")"
            case ["F,OR", *conds]:
                translated = [translate(part) for part in conds]
                return "(" + " || ".join(translated) + ")"
            case ["F,ROWCOUNT", o]:
                return f"{translate(o)}.rowcount()"
            case ["F,TODATE", d, str(format)]:
                return f"{translate(d)}.todate({format})"
            case ["F,CHR", str(code)] if code.isdigit():
                return f"char '{chr(int(code))}' {code}"
            case ["F,CURSORINDEX", str(src)]:
                return f"{src}.cursorindex()"
            case ["F,SUBSTR", exp, beg, count]:
                return f"{translate(exp)}.substr({translate(beg)}, {translate(count)})"
            case ["F,INSTR", haystack, needle, then, else_]:
                return f"{translate(needle)} in_string {translate(haystack)} ? {translate(then)} : {translate(else_)}"
            case ["F,RIGHT", exp, count]:
                return f"{translate(exp)}[-{translate(count)}:]"
            case ["F,LEFT", exp, count]:
                return f"{translate(exp)}[:{translate(count)}]"
            case ["F,REGEXP_STRING", s, pat]:
                return f"{translate(s)}.re_search({translate(pat)})"
            case ["F,REGEXP_POSITION", s, pat]:
                return f"{translate(s)}.re_search_pos({translate(pat)})"

            case [str(func)] if func in nullary_funcs:
                return f"{func.removeprefix('F,')}()".lower()

            case [str(func), param] if func.startswith(","):
                return f"{translate(param)}.pipe({func})"
            case [str(func), *rest] if func in nnary_funcs:
                match nnary_funcs[func]:
                    case int(n):
                        arity = (n, n)
                    case (int(begg), int(endd)):
                        arity = (begg, endd)

                if not arity[0] <= len(rest) <= arity[1]:
                    self.errors.append(
                        f"Invalid number of arguments for {func} - got {len(rest)}, expected {nnary_funcs[func]}"
                    )
                name = f"{func.removeprefix('F,')}".lower()
                joined = "; ".join(translate(part) for part in rest)
                return f"{name}({joined})"

            case [str(func), *rest]:
                newname = func.removeprefix("F,")
                self.errors.append(f"Unknown function {func} ({len(rest)} arguments)")
                return f"~(~{newname}(" + ";".join(translate(r) for r in rest) + ")~)~"
            case [*parts]:
                self.errors.append(f"Unknown pattern {parts}")
                return "~(~" + str(parts) + "~)~"

        s = f"Unmatched pattern {tree}"
        raise ParseError(s)


def parse(s: str, expand_entities: bool = True) -> RecursiveList[str]:
    if expand_entities:
        s = expand_xml_entities(s)
    tokens = tokenize(s)
    parsed, _ = emit_nested_sequence(tokens)
    return parsed


def expand_xml_entities(xml_string: str) -> str:
    entity_pattern = re.compile(r"&([^;]+);")

    def replace_entity(match: re.Match[str]) -> str:
        entity = match.group(1)
        if entity == "lt":
            return "<"
        elif entity == "gt":
            return ">"
        elif entity == "amp":
            return "&"
        elif entity == "quot":
            return '"'
        else:
            return match.group(0)

    return entity_pattern.sub(replace_entity, xml_string)
