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

def formatLogTable(L, mode='hex'):
    def getHex(n):
        return hex(n)[2:].zfill(2)
    LEN = 16
    rL = list()
    
    # since log doesn't have 0 value skip for both
    for i in range(0, len(L), LEN):
        line = L[i:i+LEN]
        if i == 0:  value = line.pop(0)
        if mode == 'hex':
            sL = [getHex(n) for n in line]
        elif mode == 'int':
            sL = [str(n).rjust(3) for n in line]
        if i == 0:
            sL.insert(0,'  ')
        rL.append(' '.join(sL))
    return '\n'.join(rL)

def normalized(n):
    #  mod 100011011 but only if
    # n >= 100000000
    if n < 256:
        return n
    return (n % 256) ^ 27

def x1(n):
    return n

def x2(n):
    r = n << 1
    return normalized(r)

def x3(n):
    r = (n << 1) ^ n
    return normalized(r) 

def x4(n):
    r = x2(x2(n))
    return normalized(r)

def x5(n):
    r = x4(n) ^ n
    return normalized(r)

def x7(n):
    r = x4(n) ^ x3(n) ^ n
    return normalized(r)
    
def x8(n):
    r = x2(x4(n))
    return normalized(r)

def f(n):
    r = x8(n) ^ x3(n)
    return normalized(r)

def field_generator(f):
    n = 1
    while True:
        yield n
        n = f(n)

def makeLogs(expL):
    logL = [None] * 256
    for i in range(256):
        v = expL[i]
        logL[v] = i
    logL[1] = 0
    return logL

# to use the field generator we pass in the appropriate
# function to multiply by some integer

g3 = field_generator(x3)
L3 = [g3.next() for i in range(256)]

g5 = field_generator(x5)
L5 = [g5.next() for i in range(256)]
# print len(set(L5))

# print formatTable(L5)
# print 

logL = makeLogs(L5)
# print formatLogTable(logL)

def test(f):
    g = field_generator(f)
    g.next()   # 1
    count = 1
    while True:
        v = g.next()
        if v == 1:
            break
        count += 1
    return count

print test(f)








