import decimal

tokens = (
  # type
  'IDENTIFIER',
  #'SYMBOL',
  'NUMBER',
  'STRING',
  # flow
  'WS',
  'IF',
  'ELSE',
  'FOR',
  'WHILE',
  # unary / binary operations
  'EQ',
  'NEQ',
  'ASSIGN',
  'LT',
  'LTE',
  'GT',
  'GTE',
  'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
  # sugar
  'LPAR',
  'RPAR',
  'LBRA',
  'RBRA',
  'LCBRA',
  'RCBRA',
  'COMMA',
  'COLON',
  'RETURN',
  'BACKSLASH',
  'NEWLINE',

  'SEMICOLON',
  'INDENT',
  'DEDENT',
  'END',
)
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_LT = r'\<'
t_LTE = r'\<\='
t_GT = r'\>'
t_GTE = r'\>\='
t_EQ = r'=='
t_NEQ = r'\<\>'
t_ASSIGN = r'\='
t_COLON = r':'
t_COMMA = r','
t_LBRA = r'\['
t_RBRA = r']'
t_LCBRA = r'{'
t_RCBRA = r'}'
t_SEMICOLON = r';'
t_BACKSLASH = r'\\'

# Transform reserved identifiers
RESERVED = {
  'if': 'IF',
  'return': 'RETURN',
  #'sym': 'SYMBOL'
}

def t_NUMBER(t):
  r"""(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""
  t.value = t.value
  return t

def t_STRING(t):
  r"'([^\\']+|\\'|\\\\)*'"
  t.value = t.value[1:-1]
  return t

# This needs to be before t_WS due to "if ... //comment"
def t_comment(t):
  r"[ ]*//(\\\n|[^\n])*[\n]*"
  t.lexer.lineno += len(t.value.split('\n')) - 1

def t_WS(t): # Whitespace
  r'[ ]+'
  if t.lexer.at_line_start and t.lexer.paren_count == 0:
    return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  t.type = "NEWLINE"
  if t.lexer.paren_count == 0:
    return t

def t_LPAR(t):
  r'\('
  t.lexer.paren_count += 1
  return t

def t_RPAR(t):
  r'\)'
  t.lexer.paren_count -= 1
  return t

def t_IDENTIFIER(t):
  r'[\w_][_\-\.\w0-9]*'
  t.type = RESERVED.get(t.value, "IDENTIFIER")
  return t

def t_error(t):
  #raise SyntaxError("Unknown symbol %r" % (t.value[0],))
  print("Skipping unknown symbol ", repr(t.value[0]))
  t.lexer.skip(1)
