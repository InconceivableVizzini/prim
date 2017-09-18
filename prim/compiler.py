from ply import *
from .lexer import *
from .parser import *

def compile(code):
  lexer = IndentLexer()
  parser = yacc.yacc(start="program")

  lexer.input(code)
  parser.parse(lexer=lexer)


  #tree = ast.Module(None, parser.parse(lexer=lexer))
  #print('AST: ', tree)
