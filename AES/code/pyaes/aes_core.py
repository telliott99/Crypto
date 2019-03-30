# byte is just an int
# an aes word is a list of 4 bytes
# an aes block or key is a list of 4 words

# key schedule is a flat list of 44 words 
# first schedule[:4] is the initial key

import sys
import aes_utils as ut
import aes_key as ak
import aes_info, aes_matrix
SZ = 16

#----------------------------------------

# input block or key list kL is 
# a slice of the whole key schedule
# grouped into four words, each word of 4 bytes
# the input plaintext is formatted the same

def doRound0(initial_key, kL):
    rL = ut.xorWordLists(initial_key, kL)
    print "round  0: ",
    ak.printHex(rL),
    return rL
    
# input is a list of 4 bytes, ints in 0..255
def mixOneColumn(word, mode = 'encrypt'):
    eM = aes_info.encrypt_matrix
    dM = aes_info.decrypt_matrix
    if mode == 'encrypt':
        m = eM
    else:
        m = dM
    return aes_matrix.matrixMultiply(m, word)

def mixColumnsEncrypting(kL):
    # works on one 4-byte word at a time
    f = mixOneColumn
    
    # recall what we're doing
    # 2  3  1  1     b1         o1
    # 1  2  3  1     b2    ->   o2  
    # 1  1  2  3     b3         o3
    # 3  1  1  2     b4         o4

    rL = [f(w) for w in kL]
    # ak.printHex(rL)
    return rL
    
def mixColumnsDecrypting(kL):
    # works on one 4-byte word at a time
    f = mixOneColumn
    
    # 14 11 13  9
    #  9 14 11 13
    # 13  9 14 11
    # 11 13  9 14

    rL = [f(w, mode='decrypt') for w in kL]
    # ak.printHex(rL)
    return rL

#----------------------------------------

def doOneRoundEncrypt(input, kL, last = False):
    # first step is SubstituteBytes
    SBox = aes_info.AES_Sbox_encrypt
    sL = list()
    for word in input:
        sL.append([SBox[n] for n in word])
    
    # step 2 is ShiftRows
    # rather than fool with an array do it flattened
    iL = [0, 5, 10, 15, 4, 9, 14, 3,  
          8, 13, 2, 7, 12, 1, 6, 11]
    
    flatL = list()
    for w in sL:
        flatL.extend(w)      
    rL = [flatL[i] for i in iL]
    rL = ut.chunks(rL, n=4)
    
    # step 3 is MixColumns
    # skip in round 10
    if not last:
        rL = mixColumnsEncrypting(rL)
    
    # step 4 is AddRoundKey
    # just XOR with the round key
    result = ut.xorWordLists(rL, kL)
    return result
    
def doOneRoundDecrypt(input, kL, last = False):
    # step 1 is InvShiftRows
    iL = [0, 13, 10, 7, 4, 1, 14, 11,  
          8, 5, 2, 15, 12, 9, 6, 3]
    flatL = list()
    for w in input:
        flatL.extend(w)      
    rL = [flatL[i] for i in iL]
    rL = ut.chunks(rL, n=4)
    
    # step 2 is InvSubBytes 
    SBox = aes_info.AES_Sbox_decrypt
       
    sL = list()
    for word in rL:
        sub = [SBox[n] for n in word]
        sL.append(sub)
    rL = sL
    
    # step 3 is AddRoundKey
    rL = ut.xorWordLists(rL, kL)
        
    # step 4 is InvMixColumns
    # skip in round 10
    if not last:
        rL = mixColumnsDecrypting(rL)
     
    return rL
