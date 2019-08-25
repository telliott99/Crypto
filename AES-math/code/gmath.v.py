import sys
v = False

def gmod(n,N):
    D = { 3:19, 4:25, 8:283 }
    P = D[N]
    if v:  print("gmod(%d,%d)" % (n,P))
    b = len(bin(P))
    while True:
        if n < N**2:
            return n
        m = n ^ (P << (len(bin(n)) - b))
        if v:  print("%d mod %d = %d" % (n,m,P))
        n = m

def gmultiply(a,b,N=8):  # default N = 8
    if v:  print("gmul(%d,%d)" % (a,b))
    a_in = a
    s = bin(b)[2:][::-1]   
    r = 0
    for c in s:
        if c == '1':
            r = r ^ a
        a = a << 1
    if v:  print("%d * %d = %d" %(a_in,b,r))
    return gmod(r,N)

if __name__ == "__main__":
    L = [int(c) for c in sys.argv[1:]]
    N,a,b = L
    ret = gmultiply(a,b,N=N)
    if v:  print("answer: %d" % ret)

