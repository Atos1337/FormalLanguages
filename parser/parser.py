import ply.lex as lex
import sys

tokens = [
  'OPEN',
  'CLOSE',
  'CONSTRUCT',
  'POINT',
  'ID',
  'CONJ',
  'DISJ'
]

t_OPEN = r'\('
t_CLOSE = r'\)'
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

class Parser:
  def __init__(self, s):
    self.toks = []
    lexer = lex.lex()
    lexer.input(s)
    while True:
      tok = lexer.token()
      if not tok:
        break
      self.toks.append(tok)

  def parse(self):
    i, res = self.attitude(0)
    if res is None:
      return self.toks[i], False
    else:
      return None, True

  def Id(self, i):
    if self.toks[i].type == 'OPEN':
      i += 1
      if i == len(self.toks):
        return i - 1, None
      i, res = self.body(i)
      if res is None:
        return i, None
      if i == len(self.toks):
        return i - 1, None
      if self.toks[i].type == 'CLOSE':
        return i + 1, True
      else:
        return i, None
    if self.toks[i].type == 'ID':
      return i + 1, True
    return i, None

  def conj(self, i):
    i, res = self.Id(i)
    if res is None:
      return i, None
    if i == len(self.toks):
      return i - 1, None
    if self.toks[i].type == 'CONJ':
      i += 1
      if i == len(self.toks):
        return i - 1, None
      i, res = self.conj(i)
      if res is None:
        return i, None
      return i, True
    return i, True

  def body(self, i):
    i, res = self.conj(i)
    if res is None:
      return i, None
    if i == len(self.toks):
      return i - 1, None
    if self.toks[i].type == 'DISJ':
      i += 1
      if i == len(self.toks):
        return i - 1, None
      i, res = self.body(i)
      if res is None:
        return i, None
      return i, True
    return i, True

  def attitude(self, i):
    if i == len(self.toks):
      return i, True
    if self.toks[i].type != 'ID':
      return i, None
    i += 1
    if i == len(self.toks):
      return i - 1, None
    if self.toks[i].type == 'CONSTRUCT':
      i += 1
      if i == len(self.toks):
        return i - 1, None
      i, res = self.body(i)
      if res is None:
        return i, None
      if i == len(self.toks):
        return i - 1, None
    if self.toks[i].type != 'POINT':
      return i, None
    i += 1
    if i == len(self.toks):
      return i, True
    i, res = attitude(i)
    if res is None:
      return i, None
    return i, True

if __name__ == '__main__':
  t, res = Parser(open(sys.argv[1]).read()).parse()
  if res is True:
    print("correct code")
  else:
    print("SyntaxError: line %d, colon %d" % (t.lineno, t.lexpos))