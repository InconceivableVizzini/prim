#!/usr/bin/env python
#  ___     _
# | _ \_ _(_)__ __
# |  _/ '_| |  '  \
# |_| |_| |_|_|_|_|

from __future__ import print_function, generators

import sys
import argparse
import logging

from ply import lex

from prim import __version__
from prim.tokens import *

#     ___  ___ ___ ___ ___ ___  ___   ___ _   _ _    ___
#    / _ \| __| __/ __|_ _|   \| __| | _ \ | | | |  | __|
#   | (_) | _|| _|\__ \| || |) | _|  |   / |_| | |__| _|
#    \___/|_| |_| |___/___|___/|___| |_|_\\___/|____|___|
#
# This lexical analyzer implements off-side rule,
# meaning that whitespace at the start of lines
# is important.

def create_token(token_type, lineno, value=None):
  tok = lex.LexToken()
  tok.type = token_type
  tok.value = value
  tok.lineno = lineno
  tok.lexpos = 0
  return tok

# Track the state of new lines, to grok whitespace
# and empty lines. A backslash character will perform
# line continuation.
def newlines_filter(lexer, tokens):
  lexer.at_line_start = at_line_start = False
  lexer.at_backslash = at_backslash = False
  for token in tokens:
    token.at_line_start = at_line_start
    if token.type == "BACKSLASH" and not at_backslash:
      lexer.at_backslash = at_backslash = True
      continue
    elif token.type == "NEWLINE":
      if at_backslash:
        lexer.at_backslash = at_backslash = False
        continue
      at_line_start = True
    elif token.type == "WS":
      at_line_start = True
    else:
      at_line_start = False
    lexer.at_line_start = at_line_start
    lexer.at_backslash = at_backslash
    yield token

# Track indentation and create INDENT / DEDENT tokens
def indentation_filter(tokens):
  token = None
  depth = 0
  levels = [0]
  prev_was_ws = False

  for token in tokens:
    # Disregard whitespace, as well as empty lines.
    if token.type == "WS":
      assert depth == 0 # WS only occurs at the start of lines
      depth = len(token.value)
      prev_was_ws = True
      continue # Do not pass WS tokens to the parser
    if token.type == "NEWLINE":
      depth = 0
      if prev_was_ws or token.at_line_start:
        continue # Ignore blank lines
      yield token # But pass on any other \n
      continue
    prev_was_ws = False
    if (depth == levels[-1]):
      pass # At the same depth
    elif (depth > levels[-1]): # depth is larger than previous lvl
      levels.append(depth)
      yield create_token("INDENT", token.lineno, None)
    else:
      # Find a previous level with the same depth
      try:
        i = levels.index(depth)
      except ValueError: # The current depth is not a previous lvl
        raise IndentationError("Inconsistent indentation on line {}".format(token.lineno))
      for _ in range(i + 1, len(levels)): # DEDENT to the current depth
        yield create_token("DEDENT", token.lineno, None)
        levels.pop()
    yield token
  if len(levels) > 1: # DEDENT any remaining levels
    assert token is not None
    for _ in range(1, len(levels)):
      yield create_token("DEDENT", token.lineno, None)
      levels.pop()

def endmarker_filter(lexer):
  token = None
  tokens = iter(lexer.token, None)
  tokens = newlines_filter(lexer, tokens)
  for token in indentation_filter(tokens):
    yield token
  lineno = 1
  if token is not None:
    lineno = token.lineno
  yield create_token("END", lineno)

class IndentLexer(object):
  def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
    self.lexer = lex.lex(debug=debug, optimize=optimize,
                         lextab=lextab, reflags=reflags)
    self.token_stream = None

  def input(self, s):
    self.lexer.paren_count = 0
    self.lexer.input(s)
    self.token_stream = endmarker_filter(self.lexer)

  def token(self):
    try:
      return next(self.token_stream)
    except StopIteration:
      return None

def main(argv=None):
  arg_parser = argparse.ArgumentParser(description="Test lexical analysis.")
  arg_parser.add_argument('-v', '--version', action="version",
                          version=__version__, help="Report langauge version")
  arg_parser.add_argument('file', default=sys.stdin,
                          type=argparse.FileType('r'), nargs='?',
                          help="Prim source file.")
  args = arg_parser.parse_args(argv)

  lexer = IndentLexer()
  lexer.input(args.file.read())

  for token in iter(lexer.token, None):
    print(token)
    #print('[{}, {}, {}]'.format(token.lineno, token.type, repr(token.value)))
    
if __name__ == '__main__':
  main(sys.argv[1:])
