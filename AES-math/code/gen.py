from gmath2 import gmultiply as gm

# the field is GF(2^N)
# we pass gm(a,b,N)
N = 4

def gen(g):
    n = g
    L = [n]
    for i in range(N**2):
        n = gm(g,n,N)
        L.append(n)
    print ' '.join([str(n).rjust(2) for n in L])

for g in range(2,N**2):
    gen(g)