from itertools import pairwise, product
from discopy.frobenius import *
from discopy import python

t = Ty("")
e = Ty()
_map = Box('map', t @ t, t)
_mapmap = Box('mapmap', t @ t, t)
splitlines = Box('splitlines', e, t)
split = Box('split', e, t)
_readlines = Box('readlines', t, t)
_sorted = Box('sorted', t, t)
_subtract = Box('-', e, t)
_count = Box('count', t, t)
_sum = Box('sum', t, t)
_zip = Box('zip', t @ t, t)
_filter = Box('filter', t @ t, t)
_add = Box('add', e, t)
_abs = Box('abs', e, t)
_any = Box('any', e, t)
_len = Box('len', e, t)
_int = Box('int', e, t)
split_two = Box('split_two', t, t @ t)
split_mul = Box('split_mul', t, t)
similarity = Box('similarity', t @ t, t)
safe = Box('safe', e, t)
dampened_safe = Box('dampened_safe', e, t)

def increasing(c):
    return all(1<=b-a<=3 for a,b in pairwise(c))

def decreasing(c):
    return all(1<=a-b<=3 for a,b in pairwise(c))

def bind(a, b):
    return list((x, y) for y in b for x in a)

def safe_f(c):
    return increasing(c) or decreasing(c)

def dampened_safe_f(c):
    return any(
            increasing(c[:i]+c[i+1:])
            or decreasing(c[:i]+c[i+1:])
            for i in range(len(c)))
            
def fmap(box):
    return box @ t >> _map

F = Functor(
    lambda ob: ob,
    {
        _map: lambda a,b: list(map(a,b)),
        _mapmap: lambda a,b: list(list(map(a,x)) for x in b),
        _readlines: lambda a: open(a).readlines(),
        splitlines: lambda: lambda a: a.splitlines(),
        split: lambda: lambda a: list(a.split()),
        _sorted: lambda a: list(sorted(a)),
        _subtract: lambda: lambda a: a[0]-a[1],
        _int: lambda: int,
        _any: lambda: any,
        _len: lambda: len,
        _abs: lambda: abs,
        _count: lambda a: sum(1 for x in a),
        _sum: sum,
        _filter: lambda a,b: list(filter(a,b)),
        _zip: lambda a,b: list(zip(a,b)),
        split_two: lambda a: (
            [x.split()[0] for x in a],
            [x.split()[1] for x in a], ),
        similarity: lambda a, b: list(
            x for y in b for x in a if x==y),
        safe: lambda: safe_f,
        dampened_safe: lambda: dampened_safe_f,
    },
    cod=Category(python.Ty, python.Function))
