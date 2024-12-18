from itertools import pairwise
from discopy.frobenius import *
from discopy import python

t = Ty("")
splitlines = Box('splitlines', t, t)
split = Box('split', t, t)
split_two = Box('split_two', t, t @ t)
_sorted = Box('sorted', t, t)
add = Box('add', t @ t, t)
similarity = Box('similarity', t @ t, t)
safe = Box('safe', t, t)
dampened_safe = Box('dampened_safe', t, t)

def increasing(c):
    return all(1<=b-a<=3 for a,b in pairwise(c))

def decreasing(c):
    return all(1<=a-b<=3 for a,b in pairwise(c))

def dampened_safe_f(reports):
    return sum(
        1 for r in reports
        if any(
            increasing(r[:i]+r[i+1:])
            or decreasing(r[:i]+r[i+1:])
            for i in range(len(r))))
            
            

F = Functor(
    lambda ob: ob,
    {
        splitlines: lambda a: a.splitlines(),
        split: lambda a: [
            [int(s) for s in x.split()]
            for x in a],
        split_two: lambda a: (
            [int(x.split()[0]) for x in a],
            [int(x.split()[1]) for x in a], ),
        _sorted: lambda a: (sorted(a), ),
        add: lambda a, b: sum(
            abs(x-y) for x, y in zip(a, b)),
        similarity: lambda a, b: sum(
            x for y in b for x in a if x==y),
        safe: lambda reports: sum(
            1 for c in reports
            if increasing(c) or decreasing(c)),
        dampened_safe: dampened_safe_f,
    },
    cod=Category(python.Ty, python.Function))
