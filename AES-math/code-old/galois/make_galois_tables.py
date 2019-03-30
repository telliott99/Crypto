'''
Rules for multiplication in GF(2^8):

b x 1 = b

b x 2 =
left-shift and add a zero
if b > 127:  XOR with 27

B x 3 = (B x 2) ^ (B x 1)

B x 4 = (B x 2) x 2

With this I can make my own tables 
AES needs:  2,3,9,11,13,14
'''

import aes_utils as ut

# x2:  a table to multiply by 2
def multiplyBy2(n):
    # left shift
    m = (n << 1) % 256
    # optional XOR
    if n > 127:
        m = m ^ 27
    return m

def make2x():
    rL = list()
    for n in range(256):
        x = multiplyBy2(n)
        rL.append(x)
    return rL
            
#--------------------------------------------

def formatTable(t, mode = "int"):
    rL = list()
    for i in range(256):
        if i and i % 16 == 0:
            rL.append('\n')
        m = t[i]
        if mode == "hex":
            h = hex(m)[2:].zfill(2)
            rL.append(h + " ")
        else:
            rL.append(str(m).rjust(3) + " ")
    return ''.join(rL)

#--------------------------------------------

# could be much smarter
def makePowerOf2(pow):
    rL = list()
    for n in range(256):
        x = multiplyBy2(n)
        for i in range(pow - 1):
            x = multiplyBy2(x)
        rL.append(x)
    return rL
    
#--------------------------------------------

def reducingXOR(L):
    x = 0
    for n in L:
        x = x ^ n
    return x

def makeCombo(L):
    rL = list()
    for n in range(256):
        sL = list()
        # get the value for each binary multiplier
        for table in L:
           sL.append(table[n])
        # XOR to combine them all
        rL.append(reducingXOR(sL))
    return rL
            
#--------------------------------------------

def testSameAsWiki(title, table):
    import wiki_tables as wt

    s = formatTable(table, mode = "hex")
    # print s
    
    D = { 'x2':wt.x2, 'x3':wt.x3, 'x9':wt.x9,
          'x11':wt.x11, 'x13':wt.x13, 'x14':wt.x14 }
    
    input = D[title]
    table_data = input.strip().split('\n')
    
    L = list()
    for line in table_data:
        line = line.strip()
        if line[-1] == ',':  
            line = line[:-1]    # extra ',' except last
        hL = [h[2:] for h in line.split(',')]
        iL = [int(h,16) for h in hL]
        L.extend(iL)
    assert L == table

def testAll(xL):
    tL = ['x2','x3','x9','x11','x13','x14']
    for title, table in zip(tL,xL):
        testSameAsWiki(title, table)
        print title + ' = ' + "'''"
        print formatTable(table, mode = 'hex')
        print "'''"
        print

#--------------------------------------------

if __name__ == "__main__":
    x1 = range(256)
    x2 = make2x()
    x4 = makePowerOf2(2)
    x8 = makePowerOf2(3)
    
    x3 =  makeCombo([x2,x1])
    x9 =  makeCombo([x8,x1])
    x11 = makeCombo([x8,x2,x1])  # 1011
    x13 = makeCombo([x8,x4,x1])  # 1101
    x14 = makeCombo([x8,x4,x2])  # 1110


    xL = [x2,x3,x9,x11,x13,x14]
    testAll(xL)

    
    