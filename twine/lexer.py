from typing import Iterable
from lark import Token
import re

from twine.grammar import GRAMMAR


REGEX_MAP = [
    ("TRUE", r"true"),
    ("FALSE", r"false"),
    ("COMMA", r","),
    ("COMMENT", r"%.*"),
    ("EQUAL", r"="),
    ("F", r"f"),
    ("HAT", r"\^"),
    ("RETURNS", r"returns"),
    ("IDENTIFIER", r"[a-zA-Z$][a-zA-Z0-9_$]*"),
    ("INTEGER", r"0|[1-9][0-9]*"),
    ("LPAR", r"\("),
    ("LESS", r"<"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("PIPE", r"\|"),
    ("PLUS", r"\+"),
    ("RPAR", r"\)"),
    ("COLON", r":"),
    ("SEMICOLON", r";"),
    ("SLASH", r"/"),
    ("TILDE", r"~"),
]

def lex(src: str) -> Iterable[Token]:
    """
    Analiza o código fonte e retorna uma sequência de tokens.
    """
    #  words = src.split()
    #  for word in words:
    #      kind = classify_token(word)
    #      if kind != 'COMMENT': yield Token(kind, word)
    return GRAMMAR.lex(src)

def classify_token(word: str) -> str:
    """
    Identifica o tipo de cada token.
    """
    for (nome, regex) in REGEX_MAP:
        if re.fullmatch(regex, word):
            return nome
    raise SyntaxError(f'elemento não reconhecido: {word!r}')
