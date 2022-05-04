from lark import Token
from collections import deque
from typing import Tuple
from .lexer import lex
from .ir import IR, SExpr, Declaration

EOF = Token("EOF", "$")  
STOP = deque([EOF])

def parse_to_ir(src: str) -> IR:
    tokens = deque(lex(src))
    tokens.append(EOF)
    
    ir = program(tokens)
    if tokens != STOP:
        raise SyntaxError(f"esperava fim do arquivo: {tokens}")
    return ir

# Funções auxiliares genéricas
def peek(tokens):
    "Mostra o primeiro token da lista o None"
    return tokens[0]

def next(tokens):
    "Lê o próximo token"
    return tokens.popleft()

def read(kind, tokens):
    "Lê um token do tipo dado"
    if peek(tokens).type == kind:
        return next(tokens)
    raise SyntaxError(f"esperava {kind}, obteve {peek(tokens).type}")

def expect(lit, tokens):
    "Espera um literal"
    if peek(tokens) == lit:
        return next(tokens)
    raise SyntaxError(f"esperava {lit!r}, obteve {peek(tokens)}")

def push(token, tokens):
    "Insere token de volta no início da lista de tokens."
    tokens.appendleft(token)

# Continue sua implementação aqui
def program(tokens) -> IR:
    ir = {}
    while tokens != STOP:
        name, fn = define(tokens)
        ir[name] = fn
    return ir

def define(tokens) -> Tuple[str, Declaration]:
    """IDENTIFIER "=" "f" "(" params "returns" TYPE ")" body"""
    name = str(read("IDENTIFIER", tokens))
    expect("=", tokens)
    expect("f", tokens)
    expect("(", tokens)
    argdefs = paramter_list(tokens)
    expect("returns", tokens)
    # trocar para um TYPE
    restype = tk_to_type(str(read("IDENTIFIER", tokens)))
    expect(")", tokens)
    body_ = body(tokens)

    # Cria declaração e retorna
    decl = Declaration(args=argdefs, returns=restype, body=body_)
    return (name, decl)

def id_with_type( tokens):
    name = str(read("IDENTIFIER", tokens))
    expect(":", tokens)
    # trocar para um TYPE
    value = tk_to_type(str(read("IDENTIFIER", tokens)))
    return (name, value)

def paramter_list(tokens):
    params = []
    try:
        params.append(id_with_type(tokens))
        while True:
            expect(",", tokens)
            params.append(id_with_type(tokens))
    except SyntaxError:
        ...
    return params

def tk_to_type(tk):
    if tk == 'integer':
        return int
    return bool

def body(tokens):
    if peek(tokens).value == 'print':
        return print_expression(tokens)
    return expression(tokens)

def expression(tokens):
    sim_exp = simple_expression(tokens)
    p_value = peek(tokens).value
    if p_value in ('=', '<'):
        expect(p_value, tokens)
        return [p_value, sim_exp, expression(tokens)]
    return sim_exp

def print_expression(tokens):
    expect('print', tokens)
    expect('(', tokens)
    exp = expression(tokens)
    expect(')', tokens)
    return ['print', exp, body(tokens)]

def simple_expression(tokens):
    terms = term(tokens)
    p_value = peek(tokens).value
    if p_value in ('|', '+', '-'):
        expect(p_value, tokens)
        return [p_value, terms, simple_expression(tokens)]
    return terms

def term(tokens):
    condition = cond(tokens)
    p_value = peek(tokens).value
    if p_value in ('^', '*', '/'):
        expect(p_value, tokens)
        return [p_value, condition, term(tokens)]
    return condition

def cond(tokens):
    p_tk = peek(tokens)
    if p_tk.type == 'IF':
        return if_cond(tokens)
    elif p_tk.type == 'INTEGER':
        return int(read("INTEGER", tokens))
    elif p_tk.value in ('true', 'false'):
        return str(read("IDENTIFIER", tokens)) == 'true'
    elif p_tk.type == 'IDENTIFIER':
        value = str(read("IDENTIFIER", tokens))
        if peek(tokens).value == '(':
            return fcall(value, tokens)
        return value

    expect('(', tokens)
    condition = expression(tokens)
    expect(')', tokens)
    return condition

def fcall(value, tokens):
    expect('(', tokens)
    arguments = args(tokens)
    expect(')', tokens)
    return [value, *arguments]

def args(tokens):
    arguments = []
    try:
        arguments.append(expression(tokens))
        while True:
            expect(",", tokens)
            arguments.append(expression(tokens))
    except SyntaxError:
        ...
    return arguments

def if_cond(tokens):
    expect('if', tokens)
    expect('(', tokens)
    cond = expression(tokens)
    expect(')', tokens)
    return_value1 = expression(tokens)
    expect('else', tokens)
    return_value2 = expression(tokens)
    return ['if', cond, return_value1, return_value2]
