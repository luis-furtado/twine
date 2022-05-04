from typing import Iterable
from lark import Token
import re


REGEX_MAP = [
    ("COMMENT", r"%.*"),
    ("IDENTIFIER", r"[a-zA-Z$][a-zA-Z0-9_$]*"),
    ("INTEGER", r"0|[1-9][0-9]*"),
    ("WS", r"\s"),
    ("NEWLINE", r"\n"),
    ("MISMATCH", r"."),
]

def lex(src: str) -> Iterable[Token]:
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in REGEX_MAP)
    line_start = 0
    for mo in re.finditer(tok_regex, src):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'IDENTIFIER':
            value = str(value)
        elif kind == 'INTEGER':
            value = int(value)
        elif kind in ('WS', 'COMMENT'):
            continue
        elif kind == 'NEWLINE':
            line_start = mo.end()
            continue
        elif kind == 'MISMATCH':
            raise Exception
        yield Token(kind, value)
