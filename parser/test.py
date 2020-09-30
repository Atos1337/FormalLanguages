from parser import Parser

assert Parser("f.").parse()[1]
assert Parser("f :- g.").parse()[1]
assert Parser("f :- g, h; t.").parse()[1]
assert Parser("f :- g, (h; t).").parse()[1]
assert not Parser("f").parse()[1]
assert not Parser(":- f.").parse()[1]
assert not Parser("f :- .").parse()[1]
assert not Parser("f :- g; h, .").parse()[1]
assert not Parser("f :- (g; (f).").parse()[1]
