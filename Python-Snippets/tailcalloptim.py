def trampoline(f):
    func = f
    while (callable(func)):
        func = func()
    return func

def bindparams(f):
    def bindfunc(*args, **kwargs):
        def realfunc():
            return f(*args, **kwargs)
        return realfunc
    return bindfunc

# s : continuation
@bindparams
def fac_impl(n, s):
    return s if n <= 1 else fac_impl(n - 1, s * n)

@bindparams
def fac(n):
    return fac_impl(n, 1)

def realfac(n):
    return trampoline(fac(n))





from functools import wraps
import sys

# ref: https://www.zhihu.com/question/29717057
# ref: http://code.activestate.com/recipes/474088/
class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.
    This function fails if the decorated
    function recurses in a non-tail context.
    """
    @wraps(g)
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back \
                and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while True:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    return func

# or just sys.setrecursionlimit(N)
# or just use yield