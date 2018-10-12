import pydot

from prim.ast import *

def graph_image_of_ast(ast, filename):
  edges = graph_from_ast(ast)
  g = pydot.graph_from_edges(edges)
  g.write_png(filename, prog='dot')
