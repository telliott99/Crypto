from gmath import gmultiply as gm

def line_fmt(L,n):
    pL = [str(i).rjust(n) for i in L]
    return ' '.join(pL)

def fmt(L):
    rL = list()
    for row in L:
        rL.append(line_fmt(row,2))
    return '\n'.join(rL) + '\n'

def xor(L):
    r = 0
    for n in L:
        r = r ^ n
    return r

def dot(L1,L2):
    rL = [gm(x,y) for x,y in zip(L1,L2)]
    return xor(rL)

fM = [[2,3,1,1],
      [1,2,3,1],
      [1,1,2,3],
      [3,1,1,2]]
      
rM = [[14,11,13, 9],
      [ 9,14,11,13],
      [13, 9,14,11],
      [11,13, 9,14]]
     
      
def mmul(a,b):
    b = zip(*b)
    rL = list()
    for i in range(4):
        sL = list()
        for j in range(4):
            n = dot(a[i],b[j])
            sL.append(n)
        rL.append(sL)
    return rL
    
M = mmul(fM,fM)
print(fmt(M))

'''
 5  0  4  0
 0  5  0  4
 4  0  5  0
 0  4  0  5
'''

M = mmul(fM,M)
print(fmt(M))

'''
fM * fM = rM
14 11 13  9
 9 14 11 13
13  9 14 11
11 13  9 14
'''

M = mmul(fM,M)
print(fmt(M))

'''
fM * fM * fM = I
 1  0  0  0
 0  1  0  0
 0  0  1  0
 0  0  0  1
'''

M = mmul(fM,rM)
print(fmt(M))

'''
fM * rM = I
 1  0  0  0
 0  1  0  0
 0  0  1  0
 0  0  0  1
'''
