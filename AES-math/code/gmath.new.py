def mod(n,exp,poly):
    def nspaces(n):
        b = len(bin(poly))
        return len(bin(n)) - b
        
    while True:
        if n < 2**exp:
            return n
        n = n ^ (poly << nspaces(n))

def multiplier(exp=8,poly=283):
    # multiply is a closure, "knows" poly
    def multiply(a,b):
        # binary string, reversed
        s = bin(b)[2:][::-1]
        n = 0
        for c in s:
            if c == '1':
                n = n ^ a
            a = a << 1
        return mod(n,exp,poly)
    return multiply

def xor_reduce(L):
    r = 0
    for n in L:
        r = r ^ n
    return r

def make_powers(element,f,exp):
    p = element
    n = 1
    pL = list()
    for i in range(2**exp):
        pL.append(n)
        n = f(n,p)
    while pL:
        sL = pL[:exp]
        pL = pL[exp:]
        # print ' '.join([str(i).rjust(3) for i in sL])
        print ' '.join([hex(i)[2:].zfill(2) for i in sL])

def go(exp,poly,gen):
    f = multiplier(exp=exp,poly=poly)
    make_powers(gen,f,exp)
 

if __name__ == "__main__":
    exp = 8
    poly = 283
    gen = 3
    go(exp,poly,gen)