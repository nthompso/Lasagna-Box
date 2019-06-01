# Don't read any of this code

import inspect
from typing import *

def tokenize(s, seps):
    curr = s.split()
    for sep in seps:
        split = lambda c:  [item for sublist in [[e,sep] for e in c.split(sep)] for item in sublist][:-1]
        curr = [split(c) for c in curr]
        curr = [item for sublist in curr for item in sublist]
        curr = [e for e in curr if e is not '']
    return curr

def gen_parser(f, is_method=True):
    arg_spec = inspect.getfullargspec(f)
    spec = []
    names = arg_spec.args[is_method:]
    for name in names:
        if name in arg_spec.annotations:
            spec.append(arg_spec.annotations[name])
        else:
            raise Exception(f"Please provide a type for '{name}'")
    def parse(inp):
        args = []
        tokens = tokenize(inp, [",", "]", "["])
        for t in spec:
            if t == str:
                args.append(tokens.pop(0))
                continue
            if t == int:
                args.append(int(tokens.pop(0)))
                continue
            if t == float:
                args.append(float(tokens.pop(0)))
                continue
            if t.__origin__ is list:
                assert tokens.pop(0) == "["
                l = []
                sub_t = t.__args__[0]
                while True:
                    t = tokens.pop(0)
                    if t == "]":
                        break
                    if t == ",":
                        continue
                    if sub_t == int:
                        l.append(int(t))
                    if sub_t == float:
                        l.append(float(t))
                args.append(l)
                continue
            raise Exception(f"Cannot parse type '{t}'")
        return args
    return parse, zip(names, spec)

# Tests
if __name__ == "__main__":
    def greeting(name: str, boo: int, c:float, d: List[float]) -> str:
        return 'Hello ' + name

    p = gen_parser(greeting)
    args = p("hey! 1 3.4 [1,2,3]")
    assert args == ['hey!', 1, 3.4, [1.0, 2.0, 3.0]]
    print("passed.")
