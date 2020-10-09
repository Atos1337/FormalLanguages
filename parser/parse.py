import ply.yacc as yacc
import sys

from lex import tokens

class Node:
    def __init__(self, name, *objs):
        self.name = name
        self.leaves = []
        for i in objs:
            self.leaves.append(i)

    def __str__(self):
        res =  self.name + " ("
        for i in self.leaves:
            res += str(i) + ", "
        res = res[0 : -2]
        res += ")"
        return res

def p_prog(p):
    '''prog : declaration prog
            | declaration'''
    if len(p) == 3:
        p[0] = Node("Prog", p[1], p[2])
    else:
        p[0] = Node("Prog", p[1])

def p_declaration(p):
    '''declaration : head CONSTRUCT body POINT
                   | head POINT'''
    if len(p) == 5:
        p[0] = Node("Declaration", p[1], p[3])
    else:
        p[0] = Node("Declaration", p[1])

def p_head(p):
    '''head : ID atom
            | ID'''
    if len(p) == 3:
        p[0] = Node("Head", Node("Atom", "ID " + str(p[1]), p[2]))
    else:
        p[0] = Node("Head", "ID " + str(p[1]))

def p_atom(p):
    '''atom : LBR atom RBR
            | ID atom
            | ID '''
    if len(p) == 3:
        p[0] = Node("Atom","ID " + str(p[1]), p[2])
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Node("Atom", "ID " + str(p[1]))

def p_body(p):
    '''body : disj'''
    p[0] = Node("Body", p[1])

def p_disj(p):
    '''disj : conj DISJ disj
            | conj'''
    if len(p) == 4:
        p[0] = Node("Disj", p[1], p[3])
    else:
        p[0] = p[1]

def p_id(p):
    '''id : LBR disj RBR
          | atom'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_conj(p):
    '''conj : id CONJ conj
            | id
    '''
    if len(p) == 4:
        p[0] = Node("Conj", p[1], p[3])
    else:
        p[0] = p[1]

def p_error(p):
    if p is None:
        print("SyntaxError, expected end of the declaration")
    else:
        print("SyntaxError: line %d, colon %d" % (p.lineno, p.lexpos), file=output)

parser = yacc.yacc()

s = open(sys.argv[1]).read()
output = sys.argv[1] + ".out"
output = open(output, 'w')
result = parser.parse(s)
print(result, file=output)
