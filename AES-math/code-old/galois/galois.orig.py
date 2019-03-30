import utils as ut
import aes_info
import re
from random import choice as ch

def getOneTable(t):
    input = t.strip()
    # split on space or newline
    input = re.split(' |,',input)
    # do our math with ints
    return [int(h,16) for h in input]
    
def getTimesTables():
    # for now, I have left the tables in hex
    D = dict()
    D[2] =  getOneTable(aes_info.x2)
    D[3] =  getOneTable(aes_info.x3)
    D[9] =  getOneTable(aes_info.x9)
    D[11] = getOneTable(aes_info.x11)
    D[13] = getOneTable(aes_info.x13)
    D[14] = getOneTable(aes_info.x14)
    return D

def getTheOtherStuff():
    d = aes_info.test_data
    wL = list()
    for e in d.strip().split('\n'):
        wL.append(e.strip())
    
    em = aes_info.matrix_encrypt
    emL = list()
    for e in em.strip().split('\n'):
        line = e.strip().split()
        emL.append([int(c) for c in line])
    
    dm = aes_info.matrix_decrypt
    dmL = list()
    for e in dm.strip().split('\n'):
        line = e.strip().split()
        dmL.append([int(c) for c in line])
    return wL, emL, dmL

#-------------------------------------

# input is a list of 4 bytes, ints in 0..255
def mixColumn(wL, mode = 'encrypt'):
    global eM, dM
    global tables
    
    rL = list()
    M = eM  # encrypt_matrix    
    if mode == 'decrypt':
        M = dM

    # for each position in the output vector
    # there is a corresponding matrix row
    for m in M:
   
        sL = list()
        # zip each entry in the matrix row 
        # to a value in the word
        for index, value in zip(m, wL):
            # get the table and do lookup
            if index == 1:
                sL.append(value)
            else:
                t = tables[index]
                # table data are '\xae' etc.
                sL.append(int(t[value]))
        
        # XOR the list of ints
        result = 0
        for n in sL:
            result = result ^ n
        rL.append(result)
    return rL

def getHex(L):
    return ' '.join([hex(n)[2:].zfill(2) for n in L])

def printOneRun(s, L, eL, dL):
    print "s:   ", s
    print "in:  ", getHex(L), L
    print "enc: ", getHex(eL), eL
    print "dec: ", getHex(dL), dL
    print

def doExamples():
    global examples
    for ex in examples:
    # ex = 'db 13 53 45 -> 8e 4d a1 bc'
        s = ex.split('->')[0].strip()
        # s = 'db 13 53 45'
        L = [int(b,16) for b in s.split()]
        eL = mixColumn(L)
        dL = mixColumn(eL, mode = 'decrypt')
        printOneRun(s, L, eL, dL)
        
def testRandom(n):
    R = range(256)
    for i in range(n):
        w = [ch(R) for j in range(4)]
        enc = mixColumn(w)
        dec = mixColumn(enc, mode = "decrypt")
        if not w == dec:
           print "failed with", w, enc, dec
         

if __name__ == "__main__":
    tables = getTimesTables()

    # global data
    # eM encrypt matrix, dM decrypt matrix
    examples, eM,  dM = getTheOtherStuff()

    doExamples()
    # testRandom(100000)    # no failures

'''
> python galois_orig.py 
s:    db 13 53 45
in:   db 13 53 45 [219, 19, 83, 69]
enc:  8e 4d a1 bc [142, 77, 161, 188]
dec:  db 13 53 45 [219, 19, 83, 69]

s:    f2 0a 22 5c
in:   f2 0a 22 5c [242, 10, 34, 92]
enc:  9f dc 58 9d [159, 220, 88, 157]
dec:  f2 0a 22 5c [242, 10, 34, 92]

s:    01 01 01 01
in:   01 01 01 01 [1, 1, 1, 1]
enc:  01 01 01 01 [1, 1, 1, 1]
dec:  01 01 01 01 [1, 1, 1, 1]

s:    c6 c6 c6 c6
in:   c6 c6 c6 c6 [198, 198, 198, 198]
enc:  c6 c6 c6 c6 [198, 198, 198, 198]
dec:  c6 c6 c6 c6 [198, 198, 198, 198]

s:    d4 d4 d4 d5
in:   d4 d4 d4 d5 [212, 212, 212, 213]
enc:  d5 d5 d7 d6 [213, 213, 215, 214]
dec:  d4 d4 d4 d5 [212, 212, 212, 213]

s:    2d 26 31 4c
in:   2d 26 31 4c [45, 38, 49, 76]
enc:  4d 7e bd f8 [77, 126, 189, 248]
dec:  2d 26 31 4c [45, 38, 49, 76]

> 
'''
    

