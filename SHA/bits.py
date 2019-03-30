# we work with integers for calculations
# rely on Python's promotion to L
v = False

def pprint(L):
    for e in L:
        pbin(e)
    print
        
def pbin(x, s=None):
    print bin(x)[2:].zfill(w).rjust(w),
    print hex(x)[2:].zfill(w/4).ljust(17),
    print str(x).rjust(21),
    if s:
        print s
    else:
        print

#--------------------------------

# bitwise AND:  &
# make v a local var

def AND(*L):
    if v:  print "AND"
    L = list(L)
    x = L.pop(0)
    if v:  pbin(x, 'x')
    r = x
    while L:
        y = L.pop(0)
        if v:  pbin(y, 'y')
        r = r & y
        if v:  pbin(r, 'r')
    if v:  print '-' * 20
    return r

#--------------------------------

def XOR(*L):
    if v:  print 'XOR'
    L = list(L)
    x = L.pop(0)
    if v:  pbin(x, 'x')
    r = x
    while L:
        y = L.pop(0)
        if v:  pbin(y, 'y')
        r = r^y
        if v:  pbin(r, 'r')
    if v:  print '-' * 10
    return r

#--------------------------------

def OR(*L):
    if v:  print 'OR'
    L = list(L)
    x = L.pop(0)
    if v:  pbin(x, 'x')
    r = x
    while L:
        y = L.pop(0)
        if v:  pbin(y, 'y')
        r = r|y
        if v:  pbin(r, 'r')
    if v:  print '-' * 10
    return r

#--------------------------------

def NOT(x):
    rL = list()
    for b in bin(x)[2:].zfill(w):
        if b == '1':
            rL.append('0')
        else:
            rL.append('1')
    return int('0b' + ''.join(rL),2)

#--------------------------------

def ADD(*L):
    if v:  print 'ADD'
    # modulo 2^w
    N = int(2**w)
    L = list(L)
    x = L.pop(0)
    if v:  pbin(x, 'x')
    r = x
    while L:
        y = L.pop(0)
        if v:  pbin(y, 'y')
        r = r + y
        r = r % N
        if v:  pbin(r, 'r')
    r = int(r)
    if v:  print '-' * 10
    return r
    
#--------------------------------

def SHR(x,n):
    if v:  print 'SHR'
    if v:  pbin(x, 'x -> R' + str(n) )
    r = x >> n
    if v:  pbin(r, 'r')
    if v:  print '-' * 10
    return r

def SHL(x,n):
    if v:  print 'SHL'
    if v:  pbin(x, 'L' + str(n) + ' <- x' )
    r = x << n
    if v:  pbin(r, 'r')
    if v:  print '-' * 10
    return r

#--------------------------------

def ROTR(x,n):
    if v:  print 'ROTR'
    if v:  pbin(x, 'x R' + str(n) )
    
    b = bin(x)[2:].zfill(w)
    rb = b[-n:] + b[:-n]
    r = int('0b' + rb, 2)
    if v:  pbin(r,'r')
    if v:  print '-' * 10
    return r

def ROTL(x,n):
    if v:  print 'ROTL'
    if v:  pbin(x, 'x L' + str(n) )
    return ROTR(x,w-n)

#--------------------------------

def Ch(x,y,z,names='xyz'):
    if v:  print 'Ch()'
    if v:  pbin(x, names[0])
    if v:  pbin(y, names[1])
    if v:  pbin(z, names[2])
    if v:  print '---'
    # note
    notx = NOT(x)
    if v:  pbin(notx, 'NOT(x)')
    r = XOR(AND(x,y),AND(notx,z))
    # wikipedia says
    # r = OR(AND(x,y),AND(notx,z))
    if v:  pbin(r, 'Ch, r')
    if v:  print
    return r

def Maj(x,y,z,names='xyz'):
    if v:  print 'Maj()'
    if v:  pbin(x, names[0])
    if v:  pbin(y, names[1])
    if v:  pbin(z, names[2])
    if v:  print '---'
    r = XOR(AND(x,y),AND(x,z),AND(y,z))
    # wikipedia says
    # r = OR(AND(x,y),AND(x,z),AND(y,z))
    if v:  pbin(r, 'Maj, r')
    if v:  print
    return r

def Parity(x,y,z,names='xyz'):
    if v:  print 'Parity()'
    return XOR(x,y,z)

def main():    
    AND(3,5)
    AND(3,5,7,9)
    AND(31,17)
    XOR(31,17,5,127)
    ADD(1,2,3)
    ADD(254,1,2)
    SHR(255,1)
    SHR(255,7)
    SHL(1,1)
    SHL(127,1)
    SHL(255,1)
    ROTR(127,1)

if __name__ == "__main__":
    # two global vars
    # verbose for printing
    v = True
    
    # width w (# of bits)
    w = 16
    main()
