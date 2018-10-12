from llvm import *
from llvm.core import *

from .ast import Node

class Scope(object):
    def __init__(self, current_block, builder = False):
        self.current_block = current_block
        if not builder:
            self.builder = Builder.new(self.current_block)
        else:
            self.builder = builder
        self.variables = {}
        self.functions = {}

# Generate llvm intermediate representation code from
# an AST.
class CodeGenerator(object):
    def __init__(self):
        self.scopes = []
        self.block_depth = 0
        self.module = None

    def generate_ir_from_ast(self, ast):
        if ast.__class__ != Node:
            return ast
        if ast.type == "program":
            self.module = Module.new("prim")

            # C functions to expose as global functions
            c_fns = {
                "printf":
                    self.module.add_function(
                        Type.function(Type.void(),
                                      (Type.pointer(Type.int(8)),),
                                      True),
                        "printf"),
            }

            # create a main function
            pointer = Type.pointer(Type.pointer(Type.int(8)))
            fn = Type.function(Type.int(), [ Type.int(), pointer ])
            main = self.module.add_function(fn, "main")

            builder = Builder.new(main.append_basic_block("entry"))

            self.scopes.append(Scope(main, builder))

            # add C functions to the outer-most scope's
            # function list.
            for f in c_fns:
                self.scopes[-1].functions[f] = c_fns[f]

            self.generate_ir_from_ast(ast.args[0])

            self.scopes[-1].builder.ret(Constant.int(Type.int(), 0))

            return self.module
        else:
            print("Code Generator failed to grok unknown AST node type: {}".format(ast.type))
            for arg in ast.args:
                self.generate_ir_from_ast(arg)
