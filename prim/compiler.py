from ply import *

from prim import __version__

from prim.lexer import *
from prim.parser import *
from prim.generator import *

import os

def ast_from_prim_source(code):
  lexer = IndentLexer()
  lexer.input(code)

  parser = yacc.yacc(start="program")

  return parser.parse(lexer=lexer)

def intermediate_representation_from_ast(ast):
  code_generator = CodeGenerator()
  return code_generator.generate_ir_from_ast(ast)
  

def main(argv=None):
  arg_parser = argparse.ArgumentParser(description="Compile prim source file.")
  arg_parser.add_argument('-v', '--version', action="version",
                          version=__version__, help="Report compiler version.")
  arg_parser.add_argument('file', default=sys.stdin,
                          type=argparse.FileType('r'), nargs='?',
                          help="Prim source file.")
  args = arg_parser.parse_args(argv)

  ast = ast_from_prim_source(args.file.read())

  module = intermediate_representation_from_ast(ast)

  print(str(module))

  module.to_bitcode(open("tmp/out.bc", "wb"))
  os.system("llc -o=tmp/out.s tmp/out.bc")
  os.system("gcc -o a.out tmp/out.s")

if __name__ == '__main__':
  main(sys.argv[1:])
