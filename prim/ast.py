class Node(object):
  def __init__(self, t, *args):
    self.type = t
    self.args = args

  def __str__(self):
    return str(self.type) + "(" + "".join([str(i)+"\n" for i in self.args]) + "\t)"

def ast_node_to_str(node):
  if node.__class__ != Node:
    return "{} ({}) {}".format(node, id(node), node.__class__)
  return "{} ({})".format(node.type, id(node))

def graph_from_ast(ast):
  edges = []
  # For testing while figuring out reductions in the parser
  #if isinstance(node, (list,)):
  #  for i in node:
  #    edges.append((_to_str(node), _to_str(i)))
  #    edges += find_edges(i)
  #  return edges
  if ast.__class__ != Node:
    return []
  for i in ast.args:
    edges.append((ast_node_to_str(ast), ast_node_to_str(i)))
    edges += graph_from_ast(i)
  return edges
