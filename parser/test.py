from parse import *

#ident
assert isinstance(Parsers.ID.parse('aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPrRsStTuUvVwWxXyYzZ_1234567890'), Success)
assert isinstance(Parsers.ID.parse('abc'), Success)
assert not isinstance(Parsers.ID.parse('123abc'), Success)
assert not isinstance(Parsers.ID.parse('Xyz'), Success)

#var
assert isinstance(Parsers.Var.parse('Abc'), Success)
assert isinstance(Parsers.Var.parse('H'), Success)
assert isinstance(Parsers.Var.parse('AabBcCdDeEfFgGhHiIjJkKlLmMnNoOpPrRsStTuUvVwWxXyYzZ_1234567890'), Success)
assert not isinstance(Parsers.Var.parse('123abc'), Success)
assert not isinstance(Parsers.Var.parse('xyz'), Success)

#atom
assert isinstance(Parsers.funccall.parse('a b c'), Success)
assert isinstance(Parsers.funccall.parse('a (b c)'), Success)
assert isinstance(Parsers.funccall.parse('a ((b c)) d'), Success)
assert isinstance(Parsers.funccall.parse('a ((b c)) (d)'), Success)
assert isinstance(Parsers.funccall.parse('a ((b  c)) (d)'), Success)
assert isinstance(Parsers.funccall.parse('a ((b  c) ) ( d )'), Success)
assert isinstance(Parsers.funccall.parse('a((b c))(d)'), Success)
assert str(Parsers.funccall.parse('a ((b c)) (d)').value) == str(Parsers.funccall.parse('a ((b  c)) (d)').value) == str(Parsers.funccall.parse('a ((b  c) ) ( d )').value) == str(Parsers.funccall.parse('a((b c))(d)').value)
assert not isinstance(Parsers.funccall.parse('a (a'), Success)
assert not isinstance(Parsers.funccall.parse('X a'), Success)
assert not isinstance(Parsers.funccall.parse('(a)'), Success)

#relation
assert isinstance(Parsers.RelDef.parse('a.'), Success)
assert isinstance(Parsers.RelDef.parse('a b.'), Success)
assert isinstance(Parsers.RelDef.parse('a:-a.'), Success)
assert isinstance(Parsers.RelDef.parse('a :-a.'), Success)
assert isinstance(Parsers.RelDef.parse('a :- a b.'), Success)
assert isinstance(Parsers.RelDef.parse('a b :- (a b).'), Success)
assert isinstance(Parsers.RelDef.parse('a b:- a;b,c.'), Success)
assert isinstance(Parsers.RelDef.parse('a b:- (a;b),c.'), Success)
assert isinstance(Parsers.RelDef.parse('a b:- a;b;c.'), Success)
assert isinstance(Parsers.RelDef.parse('a b:- a,b,c.'), Success)
assert isinstance(Parsers.RelDef.parse('a (b (c))  :- (a b) .'), Success)
assert isinstance(Parsers.RelDef.parse('g [X] Y:-  f X Y.'), Success)
assert not isinstance(Parsers.RelDef.parse('[X] Y:-  f X Y.'), Success)


#typeexpr
assert isinstance(Parsers.Type.parse('a'), Success)
assert isinstance(Parsers.Type.parse('Y -> X'), Success)
assert isinstance(Parsers.Type.parse('(Y -> X)'), Success)
assert isinstance(Parsers.Type.parse('(A -> B) -> C'), Success)
assert isinstance(Parsers.Type.parse('A -> B -> C'), Success)
assert isinstance(Parsers.Type.parse('list (list A) -> list A -> o'), Success)
assert isinstance(Parsers.Type.parse('list (list A) -> list A -> o'), Success)
assert isinstance(Parsers.Type.parse('pair A B -> (A -> C) -> (B -> D) -> pair C D'), Success)

#type
assert isinstance(Parsers.TypeDef.parse('type a b.'), Success)
assert isinstance(Parsers.TypeDef.parse('type a b -> X.'), Success)
assert isinstance(Parsers.TypeDef.parse('type filter (A -> o) -> list a -> list a -> o.'), Success)
assert isinstance(Parsers.TypeDef.parse('type filter (A -> o) -> list A -> list A -> o.'), Success)
assert isinstance(Parsers.TypeDef.parse('type filter (A -> o) -> list A -> list A -> o.'), Success)
assert isinstance(Parsers.TypeDef.parse('type a (((b))).'), Success)
assert isinstance(Parsers.TypeDef.parse('type d a -> (((b))).'), Success)
assert not isinstance(Parsers.TypeDef.parse("type type type -> type."), Success)
assert not isinstance(Parsers.TypeDef.parse('type x -> y -> z.'), Success)
assert not isinstance(Parsers.TypeDef.parse('tupe x o.'), Success)

#list
assert isinstance(Parsers.List.parse('[]'), Success)
assert isinstance(Parsers.List.parse('[X, Y, Z]'), Success)
assert isinstance(Parsers.List.parse('[a (b c), d, Z]'), Success)
assert not isinstance(Parsers.List.parse('[,]a, b, c['), Success)
assert isinstance(Parsers.List.parse('[H | T]'), Success)
assert isinstance(Parsers.List.parse('[a (b c) | T]'), Success)
assert not isinstance(Parsers.List.parse('[H | abc]'), Success)
assert not isinstance(Parsers.List.parse('[H | A b c]'), Success)
assert isinstance(Parsers.List.parse('[[X | T] | T]'), Success)
assert isinstance(Parsers.List.parse('[[a], [b,c]]'), Success)


