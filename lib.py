from itertools import pairwise, product
from discopy.frobenius import Ty, Box, Functor, Category
from discopy import python

def fmap(box):
    return box @ l >> _map

t = Ty("")
l = Ty("list")
f = Ty("function")
e = Ty()
_map = Box('map', f @ l, l)
_mapmap = Box('lambda a,b: (list(map(a,x)) for x in b)', f @ l, l)
_splitlines = Box('lambda a: a.splitlines()', e, f)
_split = Box('str.split', e, f)
_readlines = Box('list', t, l)
_list = Box('list', e, f)
_to_list = Box('list', l, l)
_open = Box('open', t, t)
_read = Box('lambda a: a.read()', t, t)
_sorted = Box('sorted', l, l)
_subtract = Box('lambda a: a[0]-a[1]', e, f)
_or = Box('lambda a,b: lambda c: a(c) or b(c)', f @ f, f)
_equal = Box('lambda a: a[0]==a[1]', e, f)
_count = Box('lambda a: sum(1 for x in a)', l, t)
_sum = Box('sum', l, t)
_zip = Box('zip', l @ l, l)
_filter = Box('filter', f @ l, l)
_pairwise = Box('pairwise', e, f)
_first = Box('lambda a: a[0]', e, f)
_add = Box('add', e, f)
_abs = Box('abs', e, f)
_any = Box('any', e, f)
_len = Box('len', e, f)
_int = Box('int', e, f)
_transpose = Box('lambda a: tuple(map(list, zip(*a)))', l, l @ l)
_product = Box('product', l @ l, l)
_increasing = Box('lambda c: all(1<=b-a<=3 for a,b in c)', e, f)
_decreasing = Box('lambda c: all(1<=a-b<=3 for a,b in c)', e, f)
_safe = _increasing @ _decreasing >> _or
_dampened_safe = Box('dampened_safe_f', e, f)

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


EVAL = Functor(
    lambda ob: ob,
    lambda ar: lambda *a:
        eval(ar.name)(*a) if a
        else eval(ar.name),
    cod=Category(python.Ty, python.Function))
