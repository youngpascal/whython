##################################
# IMPORTS
##################################

from numbers import Number
from symbols import SymbolTable
from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from context import Context

##################################
# RUN
##################################   
global_symbol_table = SymbolTable()
global_symbol_table.set('NULL', Number(0))
global_symbol_table.set('TRUE', Number(1))
global_symbol_table.set('FALSE', Number(0))

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    #Generate Abstract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    #Run the AST through the Interpreter
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error