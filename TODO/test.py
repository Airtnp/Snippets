class A:
    def __init__(self, n):
        self.n = n

def fac(n):
    a = A(n)
    return a.n * fac(n-1)

n = fac(10)
n += fac(20)
m = [n]
k = m[n + m[0:1:2]]