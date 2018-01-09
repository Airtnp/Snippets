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


# ref: https://gist.github.com/orf/41746c53b8eda5b988c5?utm_source=qq&utm_medium=social
import functools


def tail_call(tuple_return=False):
    def __wrapper(func):

        def _optimize_partial(*args, **kwargs):
            """
            I replace the reference to the wrapped function with a functools.partial object
            so that it doesn't actually call itself upon returning, allowing us to do it instead.
            Advantages: Theoretically needs no code changes and is more understandable
            Disadvantages: Its startup overhead is higher and its a bit slower. Also can only call
                           recursively when returning, so return func(1) + func(2) will not work.
            """
            old_reference = func.func_globals[func.func_name]
            func.func_globals[func.func_name] = functools.partial(functools.partial, func)

            to_execute = functools.partial(func, *args, **kwargs)

            while isinstance(to_execute, functools.partial):
                to_execute = to_execute()

            func.func_globals[func.func_name] = old_reference
            return to_execute

        def _optimize_tuple(*args, **kwargs):
            """
            This way requires the function to return a tuple of arguments to be passed to the next
            call.
            Advantages: Very little overhead, faster than plain recursion
            Disadvantages: Needs code changes, not as readable, no support for keyword arguments (yet)
            """
            while args.__class__ is tuple:  # Faster than isinstance()!
            #while isinstance(args, tuple):
                args = func(*args)

            return args

        if tuple_return:
            functools.update_wrapper(_optimize_tuple, func)
            return _optimize_tuple
        else:
            functools.update_wrapper(_optimize_partial, func)
            return _optimize_partial

    return __wrapper


@tail_call()
def test_fib_optimize(i, current=0, next=1):
    if i == 0:
        return current
    else:
        return test_fib_optimize(i - 1, next, current + next)


@tail_call(tuple_return=True)
def test_fib_tuple_optimized(i, current=0, next=1):
    if i == 0:
        return current
    else:
        return i - 1, next, current + next,


def test_fib_no_optimize(i, current=0, next=1):
    if i == 0:
        return current
    else:
        return test_fib_no_optimize(i - 1, next, current + next)

import timeit
import sys
sys.setrecursionlimit(8000)
for func in (test_fib_optimize, test_fib_tuple_optimized, test_fib_no_optimize):
    print func.func_name, timeit.timeit(functools.partial(func, 1700), number=1000)