from typing import NamedTuple, Dict, Union, Tuple, List
from lark import InlineTransformer, Tree, Transformer, v_args


# Representa um módulo Twine
IR = Dict[str, "Declaration"]

# A lista de argumentos é uma lista de duplas (nome, tipo) para cada argumento
ArgDefs = List[Tuple[str, type]]

# Representa uma expressão Twine como S-Expression
SExpr = Union[list, str, int, bool]

# Representa o lado direito de uma declaração de função
class Declaration(NamedTuple):
    args: List[Tuple[str, type]]
    returns: str
    body: SExpr


def operator_factory(op, name):
    @v_args(inline=True)
    def operator(self, x, y):
        return [op, x, y]
   
    operator.__name__ = name
    return operator

class IrTransformer(Transformer):
    def program(self, def_list):
        defs = {}
        for definition in def_list:
            defs.update(definition)
        #  __import__('ipdb').set_trace()
        return defs

    @v_args(inline=True)
    def define(self, name, params, return_type, body):
        return {str(name): Declaration(args=params, returns=return_type, body=body)}

    def params(self, params):
        return params
    
    @v_args(inline=True)
    def param(self, name, param_type):
        return (
            self.IDENTIFIER(name),
            self.TYPE(param_type) if type(param_type) == str else param_type
        )

    def body(self, body):
        return list(body)

    @v_args(inline=True)
    def print_expression(self, value):
        return value

    @v_args(inline=True)
    def print(self, value, body):
        return ['print', value, body]

    @v_args(inline=True)
    def cond(self, cond, return_value1, return_value2):
        return ['if', cond, return_value1, return_value2]

    @v_args(inline=True)
    def fcall(self, name, arguments):
        return [name, *arguments]

    @v_args(inline=True)
    def args(self, *arguments):
        return arguments

    def TYPE (self, tk):
        if str(tk) == 'integer':
            return int
        return bool

    def IDENTIFIER(self, tk):
        return str(tk)

    def BOOLEAN(self, tk):
        return tk == 'true'

    def INTEGER(self, tk):
       return int(tk)
    
IrTransformer.add  = operator_factory('+', 'add')
IrTransformer.sub  = operator_factory('-', 'sub')
IrTransformer.div  = operator_factory('/', 'sub')
IrTransformer.mul  = operator_factory('*', 'mul')
IrTransformer.or_  = operator_factory('|', 'or')
IrTransformer.and_ = operator_factory('^', 'and')
IrTransformer.eq   = operator_factory('=', 'eq')
IrTransformer.lt   = operator_factory('<', 'lt')

def transform(tree: Tree) -> IR:
    """
    Transforma uma árvore sintática que descreve um módulo Twine
    na representação interna do código como um dicionário de definições.
    """
    return IrTransformer().transform(tree)
