import pydot

from prim.ast import Node

def _to_str(node):
  if node.__class__ != Node:
    return "{} ({})".format(node, id(node))
  return "{} ({})".format(node.type, id(node))

def find_edges(node):
  edges = []
  if node.__class__ != Node:
    return []
  for i in node.args:
    edges.append((_to_str(node), _to_str(i)))
    edges += find_edges(i)
  return edges

def graph(node, filename):
  edges = find_edges(node)
  g = pydot.graph_from_edges(edges)
  g.write_png(filename, prog='dot')
