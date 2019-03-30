# Use 0x03 as a generator to create GF(2e8)

def formatTable(L, mode='hex'):
    def getHex(n):
        return hex(n)[2:].zfill(2)
    LEN = 16
    rL = list()
    for i in range(0, len(L), LEN):
        line = L[i:i+LEN]
        if mode == 'hex':
            sL = [getHex(n) for n in line]
        elif mode == 'int':
            sL = [str(n).rjust(3) for n in line]
        rL.append(' '.join(sL))
    return '\n'.join(rL)


def normalized(n):
    #  mod 100011011 but only if
    # n >= 100000000
    if n < 256:
        return n
    return (n % 256) ^ 27

def times2(n):
    r = n << 1
    return normalized(r)

def times3(n):
    r = (n << 1) ^ n
    return normalized(r) 

def field_generator():
    n = 1
    while True:
        yield n
        n = times3(n)

g = field_generator()
expL = [g.next() for i in range(256)]
print formatTable(expL, mode='hex')

