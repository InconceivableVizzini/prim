from prim.ast import Node

def p_error(p):
  print("Syntax error on line {}, column {}, on {}.".format(p.lineno, p.lexpos, p.type))

def p_program(p):
  """program : block END"""
  p[0] = Node('program', p[1])

def p_block(p):
  """block : statements"""
  p[0] = Node('block', p[1])

def p_statements(p):
  """statements : statements NEWLINE statement
         | statement
  """
  if len(p) == 2:
    p[0] = Node('statements', p[1])
  else:
    p[0] = Node('statements', [p[1], p[2]])

def p_statement(p):
  #  """statement : assignment_statement
  #         | if_statement
  #         | while_statement
  #         | for_statement
  #         | expr
  #  """
  """statement : assignment_statement
         | if_statement
         | expr
  """
  p[0] = Node('statement', p[1])

def p_assignment_statement(p):
  """assignment_statement : IDENTIFIER ASSIGN expr
         | IDENTIFIER IDENTIFIER ASSIGN expr
  """
  if len(p) > 4:
    p[0] = Node('assignment_statement', [p[1], p[2]], p[4])
  else:
    p[0] = Node('assignment_statement', p[1], p[3])

def p_if_statement(p):
  """if_statement : IF expr NEWLINE INDENT statements DEDENT
         | IF expr COLON statement
  """
  if len(p) > 5:
    p[0] = Node('if_statement', p[2], p[5])
  else:
    p[0] = Node('if_statement', p[2], p[4])

def p_expr(p):
  """expr : procedure_call
         | equality
         | unaop
         | binop
         | NUMBER
         | IDENTIFIER
  """
  p[0] = p[1]

def p_procedure_call(p):
  """procedure_call : END
  """
  p[0] = p[1]

def p_equality(p):
  """equality : expr EQ expr
         | expr NEQ expr
         | expr LT expr
         | expr LTE expr
         | expr GT expr
         | expr GTE expr 
  """
  p[0] = Node('equality', p[2], p[1], p[3])

def p_binop(p):
  """binop : expr SUB expr
          | expr ADD expr
  """
  p[0] = Node('binop', p[2], p[1], p[3])

def p_unaop(p):
  """unaop : SUB expr
          | ADD expr
  """
  p[0] = Node('unaop', p[1], p[2])
