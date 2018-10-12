from ply import yacc

from prim import __version__

from prim.lexer import *
from prim.ast import *
from prim.productions import *
from prim.graph import *

import pprint

pp = pprint.PrettyPrinter(indent=2)

def main(argv=None):
  arg_parser = argparse.ArgumentParser(description="Graph a parsed AST.")
  arg_parser.add_argument('-v', '--version', action="version",
                          version=__version__, help="Report langauge version")
  arg_parser.add_argument('file', default=sys.stdin,
                          type=argparse.FileType('r'), nargs='?',
                          help="Prim source file.")
  args = arg_parser.parse_args(argv)

  lexer = IndentLexer()
  lexer.input(args.file.read())

  parser = yacc.yacc(start="program")

  ast = parser.parse(lexer=lexer)

  pp.pprint(graph_from_ast(ast))

  graph_image_of_ast(ast, 'ast-graph.png')
  
if __name__ == '__main__':
  main(sys.argv[1:])

