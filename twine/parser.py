from lark import Lark, Tree, Token
from pathlib import Path
from typing import Dict, Iterable

from twine.grammar import GRAMMAR


def parse(src: str) -> Tree:
    """
    Analiza o código fonte e retorna a árvore sintática Lark.
    """
    return GRAMMAR.parse(src)
