# globals
D = dict()
x2count = 0
x4count = 0

def normalized(n):
    #  mod 100011011 but only if
    # n >= 100000000
    if n < 256:
        return n
    return (n % 256) ^ 27

def x1(n):
    return n

def x2(n):
    global x2count
    if (2,n) in D:  
        x2count += 1
        return D[(2,n)]
    r = n << 1
    r = normalized(r)
    D[(2,n)] = r
    return normalized(r)

def x4(n):
    global x4count
    if (4,n) in D:  
        x4count += 1
        return D[(4,n)]
    ret = normalized(x2(x2(n)))
    D[(4,n)] = ret
    return ret
    
def x8(n):
    if (8,n) in D:  return D[(8,n)]
    ret = normalized(x2(x4(n)))
    D[(8,n)] = ret
    return ret
        
def x16(n):
    if (16,n) in D:  return D[(16,n)]
    ret = normalized(x2(x8(n)))
    D[(16,n)] = ret
    return ret
       
def x32(n):
    if (32,n) in D:  return D[(32,n)]
    ret = normalized(x2(x16(n)))
    D[(32,n)] = ret
    return ret
    
def x64(n):
    if (64,n) in D:  return D[(64,n)]
    ret = normalized(x2(x32(n)))
    D[(64,n)] = ret
    return ret
      
def x128(n):
    if (128,n) in D:  return D[(128,n)]
    ret = normalized(x2(x64(n)))
    D[(128,n)] = ret
    return ret

def timesX(x,n):
    fL = [x1,x2,x4,x8,x16,x32,x64,x128]
    bL = list(bin(x)[2:])
    bL.reverse()
    rL = list()
    for b,f in zip(bL,fL):
        if b == '1':
            rL.append(f(n))
    ret = 0
    for m in rL:
        ret = ret ^ m
    return normalized(ret)

    

