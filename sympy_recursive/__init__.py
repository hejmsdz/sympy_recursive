from sympy import *

class RecursiveResolutionError(Exception):
    pass

class Recursive(IndexedBase):
    """
    Create a new instance of Recursive sequence.
    Note that it's essential to set the index manually
    after creating the object.
    """
    def __init__(self, *args, **kwargs):
        super(Recursive, self).__init__(*args, **kwargs)
        self.index = None
        self.starting = []
        self.nth = None

    """
    Return self[index] symbolically.
    This is actually a call to the parent's __getitem__.
    """
    def sub_symbolic(self, index):
        return super(Recursive, self).__getitem__(index)

    def __getitem__(self, index):
        if index == self.index:
            # return the general n-th term formula for self[n]
            return self.nth
        else:
            try:
                # return the starting value for a[0..k]
                index_i = int(index)
                return self.starting[index_i]
            except IndexError:
                # calculate the n-th term recursively
                return self.nth.subs(self.index, index)
            except:
                # otherwise fall back to the parent, ie. return self[index] symbolically
                return self.sub_symbolic(index)

    def __setitem__(self, index, value):
        if isinstance(index, int):
            # for an integer value, set a starting value
            if index == len(self.starting):
                self.starting.append(value)
            else:
                # this may raise an IndexError
                self.starting[index] = value
        elif index is self.index:
            # set self[index]
            self.nth = value

    """
    Iterate infinitely over items of the sequence.
    """
    def __iter__(self):
        # this list will contain k last generated items of the seqence,
        # necessary to generate the next one
        items = self.starting[:]

        # yield the k first items
        for item in items:
            yield item

        n = self.index
        k = len(self.starting)

        while True:
            item = self.nth
            # substitute a[n-i] with actual numbers
            for i in range(k):
                item = item.subs(self.sub_symbolic(n-i-1), items[k-i-1]).simplify()

            # add the current item to the list and drop the first one
            items.pop(0)
            items.append(item)
            yield item

    """
    Determine an explicit formula for the nth term.
    """
    def resolve(self):
        n = self.index
        k = len(self.starting)

        # create a characteristic equation if it makes sense, ie. when:
        # c0*a[n] + c1*a[n-1] + ... + ck*a[n-k] = 0
        a_n = self.nth.as_coefficients_dict()

        dependency = {n: -1}
        # dependency will be a dict in form {n-k: ck}
        # -1 is here because we move a[n] to the other side of the equation
        for i in a_n:
            if type(i) is Indexed and i.base is self and len(i.indices) == 1:
                index, = i.indices
                coeff = a_n[i]
                dependency[index] = coeff
            else:
                raise RecursiveResolutionError("The recursion is not homogeneous.")

        r = Symbol('r')
        equation = sum(coeff*r**(k+i-n) for i, coeff in dependency.iteritems())
        # the equation looks like:
        # c0 + c1*r + c2*r^2 + ... + ck*r^k = 0
        r_ = roots(equation, r)

        # for every root, whose multiplicity is j, we add the following to the solution:
        # (x0 + x1*n + x2*n^2 + ... + xj*n^j) * root^n
        # in particular, when the root is single, it boils down to:
        # x0 * root^n
        # x0..xk are some constants coefficients that will be figured out later
        solution = 0
        x = IndexedBase('x')
        x_index = 0
        for root, j in r_.iteritems():
            solution += sum(x[x_index+i]*n**i for i in range(j))*root**n
            x_index += j

        # to calculate the coefficients, we build a system of equations,
        # using the starting items and solve it
        system = [solution.subs(n, i) - start for i, start in enumerate(self.starting)]
        xs = solve(system, *(x[i] for i in range(k)))
        #  = solve(system, x[0], x[1], ... , x[k])

        solution = solution.subs(xs)
        return solution
