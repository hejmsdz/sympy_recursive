from sympy import *
from sympy_recursive import Recursive

# create an index symbol
n = Symbol('n')

# create the sequence
fib = Recursive('fib')
fib.index = n

# input the first items
fib[0] = 1
fib[1] = 1

# provide a recursive formula
fib[n] = fib[n-1] + fib[n-2]

# resolve it
explicit = fib.resolve()

# test
for i in range(10):
    value = explicit.subs(n, i).simplify()
    print "fib[{}] = {}".format(i, value)
