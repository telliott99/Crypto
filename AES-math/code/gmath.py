def gmod(n,p):  # 283 is standard, see gmultiply
    # leave leading '0b'
    b = len(bin(p))
    
    # repeatedly
    while True:
        if n < 256:
            return n
        # shift p out to match n
        d = p << (len(bin(n)) - b)
        n = n ^ d

def gmultiply(a,b,p=283):
    # for efficiency
    # if a < b:
        # a,b = b,a
        
    # the digits of binary b (reversed)
    s = bin(b)[2:][::-1]
    
    r = 0
    # for each digit in b (reversed)
    # add a to accumulated result
    # where a is left-shifted 
    # by digit's place in b (reversed)
    for c in s:
        if c == '1':
            r = r ^ a       # addition
        a = a << 1          # left-shift
    return gmod(r,p)

