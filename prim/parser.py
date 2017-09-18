from ply import yacc

from prim import __version__

from prim.lexer import *
from prim.ast import *
from prim.productions import *
from prim.graph import *

def main(argv=None):
  arg_parser = argparse.ArgumentParser(description="Test syntactic analysis.")
  arg_parser.add_argument('-v', '--version', action="version",
                          version=__version__, help="Report langauge version")
  arg_parser.add_argument('file', default=sys.stdin,
                          type=argparse.FileType('r'), nargs='?',
                          help="Prim source file.")
  args = arg_parser.parse_args(argv)

  lexer = IndentLexer()
  lexer.input(args.file.read())

  parser = yacc.yacc(start="program")
  #parser = yacc.yacc(start="program", errorlog=yacc.NullLogger())

  ast = parser.parse(lexer=lexer)

  graph(ast, 'ast-graph.png')

if __name__ == '__main__':
  main(sys.argv[1:])

