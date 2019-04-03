# this module exercises the tables

import aes_utils as ut
import galois_hex # x2 x3 ..
import aes_info
from random import choice as ch

# multiply a matrix * word -> word
# word is [int, int, int, int]

# globals
D = galois_hex.getTimesTables()

eM = aes_info.encrypt_matrix
dM = aes_info.decrypt_matrix

def matrixMultiply(matrix, word):
    rL = list()
    for row in matrix:
        sL = list()
        for multiplier, value in zip(row,word):
            table = D[multiplier]
            sL.append(table[value])
        rL.append(ut.reducingXOR(sL))
    return rL


def testMatrixMultiply():    
    test_data = '''
        db 13 53 45 -> 8e 4d a1 bc
        f2 0a 22 5c -> 9f dc 58 9d
        01 01 01 01 -> 01 01 01 01
        c6 c6 c6 c6 -> c6 c6 c6 c6
        d4 d4 d4 d5 -> d5 d5 d7 d6
        2d 26 31 4c -> 4d 7e bd f8
        '''
    
    for line in test_data.strip().split('\n'):
        sL = line.strip().split('->')
        input =  sL[0].strip()
        output = sL[1].strip()
        
        word = [int(c,16) for c in input.split()]
        result = matrixMultiply(eM, word)
        hL = [hex(n)[2:].zfill(2) for n in result]
        hex_result = ' '.join(hL)
        
        # prints exactly what we have above
        print input, '=>',  hex_result
        
        assert output == hex_result
        

def testRandom(n):
    R = range(256)
    for i in range(n):
        w = [ch(R) for j in range(4)]
        e = matrixMultiply(eM, w)
        d = matrixMultiply(dM, e)
        assert w == d
    print "passed:  %d random tests" % n

if __name__ == "__main__":
    
    testMatrixMultiply()
    testRandom(int(1e5))

'''
> python aes_math.py 
db 13 53 45 => 8e 4d a1 bc
f2 0a 22 5c => 9f dc 58 9d
01 01 01 01 => 01 01 01 01
c6 c6 c6 c6 => c6 c6 c6 c6
d4 d4 d4 d5 => d5 d5 d7 d6
2d 26 31 4c => 4d 7e bd f8
passed:  100000 random tests
>
'''
