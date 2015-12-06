# sympy_recursive

## Introduction
On my discrete math class I learned that recursive sequences which are linear
and homogeneous can be transformed to an explicit formula using a fairly simple
algorithm. To help myself remember and understand it, I coded it in Python using
[SymPy](http://www.sympy.org/) - an amazing symbolic math library for this language.

## Usage

```python
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
```

After creating an index symbol, the sequence and assigning one to another,
you can define `k` starting items of the sequence as if it was an array.
Then, set a recursive formula at your symbolic index. To refer to previous items,
put `n-1` up to `n-k` in the square brackets. Note that the formula may not
contain anything but a sum of previous items, each multiplied by a constant.
Otherwise, no longer will the recursion be linear and homogeneous and the program
won't be able to resolve it.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
