class Node(object):
  def __init__(self, t, *args):
    self.type = t
    self.args = args

  def __str__(self):
    return str(self.type) + "(" + "".join([str(i)+"\n" for i in self.args]) + "\t)"
