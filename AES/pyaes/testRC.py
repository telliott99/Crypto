def gmod(n,p=283):
    b = len(bin(p))
    while True:
        if n < 256:
            return n
        d = p << (len(bin(n)) - b)
        n = n ^ d

def gmultiply(a,b,p=283):
    s = bin(b)[2:][::-1]    
    r = 0
    for c in s:
        if c == '1':
            r = r ^ a       # addition
        a = a << 1          # left-shift
    return gmod(r,p)

#-----------------------------------------

s = '''
1, 2, 4, 8, 16, 32, 
64, 128, 27, 54, 108, 
216, 171, 77, 154, 47
'''

def RC_generator():
    sL = s.strip().split(',')
    bL = [int(c) for c in sL]
    for b in bL:
        yield b

RC = [1]
for i in range(15):
    RC.append(gmultiply(RC[-1],2))

s2 = str(RC)
s3 = str(list(RC_generator()))
assert s2 == s3