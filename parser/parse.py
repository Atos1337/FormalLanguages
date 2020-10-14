import sys
from parsita import *

def printlist(xs):
    if len(xs) == 0:
        return 'nil'
    else:
        res = 'cons (' + str(xs[0]) + ') '
        if len(xs) == 1:
            res += 'nil'
        else:
            res += '(' + printlist(xs[1:]) + ')'
        return res

class Node:
    def __init__(self, name, objs):
        self.name = name
        self.leaves = objs

    def __str__(self):
        if self.name == "List":
            if len(self.leaves) < 2:
                return printlist(self.leaves)
            if self.leaves[1] == '|':
                return 'cons (' + str(self.leaves[0]) + ') (' + str(self.leaves[2]) + ')'
            else:
                return printlist(self.leaves)
        if len(self.leaves) == 1:
            if (self.name == "Type" and (len(self.leaves[0].leaves) == 1 or self.leaves[0].name == self.name)):
                return str(self.leaves[0])
            return self.name + ' ' + str(self.leaves[0])
        res =  self.name + " ("
        for i in self.leaves:
            res += str(i) + ", "
        res = res[0 : -2]
        res += ")"
        return res

def rd(x):
    if isinstance(x, list):
        x[0].name = "Head " + x[0].name
        x[1].name = "Body " + x[1].name
        return Node("RelDef", x)
    else:
        x.name = "Head " + x.name
        return Node("RelDef", [x])

def fc(x):
    if len(x[1]) == 0:
        return x[0]
    else:
        return Node("Atom", [x[0]] + x[1])

def f(x):
    if isinstance(x, list):
        return Node("Atom", x)
    else:
        return x

def Disj(x):
   if isinstance(x, list):
       return Node("Disj", x)
   else:
       return x

def Conj(x):
   if isinstance(x, list):
       return Node("Conj", x)
   else:
       return x

def printFile(res, output):
    if isinstance(res, Success):
        print(res.value, file=output)
    else:
        print(res.message, file=output)


class Parsers(TextParsers, whitespace = r'[ \t\n\r]*'):
    ID = reg(r'(?!module)(?!type)[a-z_][A-Za-z0-9_]*') > (lambda x: Node("ID", [x]))
    #Переменная
    Var = reg(r'(?!module)(?!type)[A-Z][A-Za-z0-9_]*') > (lambda x: Node("Var", [x]))
    #База
    RelDef = (funccall << lit(':-') & disj | funccall) << lit('.') > (lambda x: rd(x))
    funccall = ID & rep(fib) > (lambda x: fc(x))
    fib = lit('(') >> fib << lit(')') | b | Var | List | ID > (lambda x: f(x))
    b = lit('(') >> (funccall | Var | List) << lit(')') > (lambda x: x)
    finb = lit('(') >> finb << lit(')') | funccall > (lambda x: x)
    disj = conj << ';' & disj | conj > (lambda x: Disj(x))
    id = lit('(') >> disj << lit(')') | finb > (lambda x: x)
    conj = id << ',' & conj | id > (lambda x: Conj(x))
    #Модуль
    ModDef = lit('module') >> ID << lit('.') > (lambda x: Node("Module", [x]))
    #Типы
    TypeDef = lit('type') >> ID & Type << lit('.') > (lambda x: Node("Typedef", x))
    Type = rep1sep((lit('(') >> Type << lit(')') | funccall | Var), lit('->')) > (lambda x: Node("Type", x))
    #Списки
    List = lit('[') >> repsep((List | funccall | Var), ',') << lit(']') | lit('[') >> (Var | funccall | List) & lit('|') & Var << lit(']') > (lambda x: Node("List", x))
    #Парсер всей программы
    prog = rep(ModDef) & rep(TypeDef) & rep(RelDef) > (lambda x: Node("Prog", x[0] + x[1] + x[2]))

if __name__ == "__main__":
    output = ''
    if len(sys.argv) == 3:
        output = open(sys.argv[2] + '.out', 'w')
    else:
        output = open(sys.argv[1] + '.out', 'w')
    if sys.argv[1] == '--atom':
        printFile(Parsers.funccall.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--typeexpr':
        printFile(Parsers.Type.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--type':
        printFile(Parsers.TypeDef.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--module':
        printFile(Parsers.ModDef.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--relation':
        printFile(Parsers.RelDef.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--list':
        printFile(Parsers.List.parse(open(sys.argv[2]).read()), output)
    elif sys.argv[1] == '--prog':
        printFile(Parsers.prog.parse(open(sys.argv[2]).read()), output)
    else:
        printFile(Parsers.prog.parse(open(sys.argv[1]).read()), output)
