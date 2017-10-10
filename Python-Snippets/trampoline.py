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

