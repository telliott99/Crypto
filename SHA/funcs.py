from bits import *

# ------------------------
# Constants

# for SHA-1 K constants
K0  = '5a827999'
K20 = '6ed9eba1'
K40 = '8f1bbcdc'
K60 = 'ca62c1d6'

# for SHA-1 H (register) constants
H0 = '67452301'
H1 = 'efcdab89'
H2 = '98badcfe'
H3 = '10325476'
H4 = 'c3d2e1f0'

# constants derived from
# from sqrt(n), n = 2, 3, .. 19
# for SHA-256 and -512 H (register) constants
magic1 = '''
 2 6a09e667f3bcc908
 3 bb67ae8584caa73b
 5 3c6ef372fe94f82b
 7 a54ff53a5f1d36f1
11 510e527fade682d1
13 9b05688c2b3e6c1f
17 1f83d9abfb41bd6b
19 5be0cd19137e2179
'''

def getRegisterConstants():
    rL = list()
    L = magic1.strip().split()
    for i in range(1,len(L),2):
        rL.append(L[i].strip())
    return rL

# constants derived from 
# cube_root(n), n = 2, 3, .. 409
# for SHA-256 and -512 K constants
magic2 = '''
  2 428a2f98d728ae22
  3 7137449123ef65cd
  5 b5c0fbcfec4d3b2f
  7 e9b5dba58189dbbc
 11 3956c25bf348b538
 13 59f111f1b605d019
 17 923f82a4af194f9b
 19 ab1c5ed5da6d8118
 23 d807aa98a3030242
 29 12835b0145706fbe
 31 243185be4ee4b28c
 37 550c7dc3d5ffb4e2
 41 72be5d74f27b896f
 43 80deb1fe3b1696b1
 47 9bdc06a725c71235
 53 c19bf174cf692694
 59 e49b69c19ef14ad2
 61 efbe4786384f25e3
 67 0fc19dc68b8cd5b5
 71 240ca1cc77ac9c65
 73 2de92c6f592b0275
 79 4a7484aa6ea6e483
 83 5cb0a9dcbd41fbd4
 89 76f988da831153b5
 97 983e5152ee66dfab
101 a831c66d2db43210
103 b00327c898fb213f
107 bf597fc7beef0ee4
109 c6e00bf33da88fc2
113 d5a79147930aa725
127 06ca6351e003826f
131 142929670a0e6e70
137 27b70a8546d22ffc
139 2e1b21385c26c926
149 4d2c6dfc5ac42aed
151 53380d139d95b3df
157 650a73548baf63de
163 766a0abb3c77b2a8
167 81c2c92e47edaee6
173 92722c851482353b
179 a2bfe8a14cf10364
181 a81a664bbc423001
191 c24b8b70d0f89791
193 c76c51a30654be30
197 d192e819d6ef5218
199 d69906245565a910
211 f40e35855771202a
223 106aa07032bbd1b8
227 19a4c116b8d2d0c8
229 1e376c085141ab53
233 2748774cdf8eeb99
239 34b0bcb5e19b48a8
241 391c0cb3c5c95a63
251 4ed8aa4ae3418acb
257 5b9cca4f7763e373
263 682e6ff3d6b2b8a3
269 748f82ee5defb2fc
271 78a5636f43172f60
277 84c87814a1f0ab72
281 8cc702081a6439ec
283 90befffa23631e28
293 a4506cebde82bde9
307 bef9a3f7b2c67915
311 c67178f2e372532b
313 ca273eceea26619c
317 d186b8c721c0c207
331 eada7dd6cde0eb1e
337 f57d4f7fee6ed178
347 06f067aa72176fba
349 0a637dc5a2c898a6
353 113f9804bef90dae
359 1b710b35131c471b
367 28db77f523047d84
373 32caab7b40c72493
379 3c9ebe0a15c9bebc
383 431d67c49c100d4c
389 4cc5d4becb3e42b6
397 597f299cfc657e2a
401 5fcb6fab3ad6faec
409 6c44198c4a475817
'''

def getKConstants():
    rL = list()
    L = magic2.strip().split()
    for i in range(1,len(L),2):
        rL.append(L[i].strip())
    return rL

# ------------------------

# Functions

def S0_256(x):
    r2 = ROTR(x, 2)
    r13 = ROTR(x, 13)
    r22 = ROTR(x, 22)
    r = XOR(r2,r13,r22)
    return r

def S1_256(x):
    r6 = ROTR(x, 6)
    r11 = ROTR(x, 11)
    r25 = ROTR(x, 25)
    r = XOR(r6,r11,r25)
    return r

def s0_256(x):
    r7 = ROTR(x,7)
    r18 = ROTR(x,18)
    sh3 = SHR(x,3)
    r = XOR(r7,r18,sh3)
    return r

def s1_256(x):
    r17 = ROTR(x,17)
    r19 = ROTR(x,19)
    sh10 = SHR(x,10)
    r = XOR(r17,r19,sh10)
    return r
     
#---------------

def S0_512(x):
    r28 = ROTR(x, 28)
    r34 = ROTR(x, 34)
    r39 = ROTR(x, 39)
    r = XOR(r28,r34,r39)
    return r

def S1_512(x):
    r14 = ROTR(x, 14)
    r18 = ROTR(x, 18)
    r41 = ROTR(x, 41)
    r = XOR(r14,r18,r41)
    return r

def s0_512(x):
    r1 = ROTR(x,1)
    r8 = ROTR(x,8)
    sh7 = SHR(x,7)
    r = XOR(r1,r8,sh7)
    return r

def s1_512(x):
    r19 = ROTR(x,19)
    r61 = ROTR(x,61)
    sh6 = SHR(x,6)
    r = XOR(r19,r61,sh6)
    return r
  
if __name__ == "__main__":
    # print getRegisterConstants()
    L = getKConstants()
    print L[:2] + L[-2:]
