import ply.lex as lex
import sys

tokens = [
  'LBR',
  'RBR',
  'CONSTRUCT',
  'POINT',
  'ID',
  'CONJ',
  'DISJ'
]

t_LBR = r'\('
t_RBR = r'\)'
t_CONSTRUCT = r':-'
t_POINT = r'\.'
t_ID = r'[A-Za-z_][A-Za-z_0-9]*'
t_CONJ = r','
t_DISJ = r';'

t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("SyntaxError: line %d, colon %d" % (t.lineno, t.lexpos))
  exit()

lexer = lex.lex()