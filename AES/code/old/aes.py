# byte is just an int
# an aes word is a list of 4 bytes
# an aes block or key is a list of 4 words

# key schedule is a flat list of 44 words 
# first schedule[:4] is the initial key
import sys
import utils as ut
import aes_info, aes_math
import aes_key as ak
SZ = 16

def testGetKeySchedule():
    s =  '00 00 00 00 00 00 00 00 '
    s += '00 00 00 00 00 00 00 00'
    schedule = getKeySchedule(s, mode = 'hex')
    # ak.printHex(schedule[-4:])

def getKeySchedule(input, mode='str'):
    if mode == 'str':
        s = ak.padKey(input)
        kL = ak.processTextKey(s)
    elif mode == 'hex':
        hL = input.strip().split()
        kL = [int(h,16) for h in hL]
    else:
        kL = input
    assert len(kL) == SZ
    kL = ut.chunks(kL,4)
    return ak.expand_key(10, kL)

def print_schedule(pL):
    pL = ut.chunks(sched, n=4)
    for i,kL in enumerate(pL):
        print str(i).rjust(2), "       ",
        ak.printHex(kL)
    print

def getMessageWords(fn):
    input = ut.readData(fn)
    pL = [ord(c) for c in input]
    return ut.chunks(pL, n=4)

# a single word is 4 bytes
def xorTwoWords(w1,w2):
    return [m^n for m,n in zip(w1,w2)]

# four words of 4 bytes each
def xorWordLists(L1,L2):
    rL = list()
    for w1,w2 in zip(L1,L2):
        rL.append(xorTwoWords(w1,w2))
    return rL

#----------------------------------------

# input block or key list kL is 
# a slice of the whole key schedule
# grouped into four words, each word of 4 bytes
# the input plaintext is formatted the same

def doRound0(initial_key, kL):
    rL = xorWordLists(initial_key, kL)
    print "round  0: ",
    ak.printHex(rL)
    return rL

def mixColumnsEncrypting(kL):
    # works on one 4-byte word at a time
    f = aes_math.mixColumn
    
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
    f = aes_math.mixColumn
    
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
    s = aes_info.AES_Sbox_encrypt
    SBox = [int(c) for c in s.strip().split()]
    
    sL = list()
    for word in input:
        sL.append([SBox[n] for n in word])
    # ak.printHex(sL)
    
    # step 2 is ShiftRows
    iL = [0, 5, 10, 15, 4, 9, 14, 3,  
          8, 13, 2, 7, 12, 1, 6, 11]
    
    flatL = list()
    for w in sL:
        flatL.extend(w)      
    rL = [flatL[i] for i in iL]
    rL = ut.chunks(rL, n=4)
    #ak.printHex(rL)
    
    # step 3 is MixColumns
    # we call out and then skip in round 10
    
    if not last:
        rL = mixColumnsEncrypting(rL)
    
    # step 4 is just XOR with the round key
    result = xorWordLists(rL, kL)
    return result
    
def doOneRoundDecrypt(input, kL, last = False):
    print "doOneRoundDecrypt"
    print "input"
    ak.printHex(input)
    print "kL"
    ak.printHex(kL)

    # step 1 is InvShiftRows
    # ak.printHex(input)
    iL = [0, 13, 10, 7, 4, 1, 14, 11,  
          8, 5, 2, 15, 12, 9, 6, 3]
    flatL = list()
    for w in input:
        flatL.extend(w)      
    rL = [flatL[i] for i in iL]
    rL = ut.chunks(rL, n=4)
    print "InverseShiftRows"
    ak.printHex(rL)
    
    # step 2 is InvSubBytes 
    s = aes_info.AES_Sbox_decrypt
    SBox = [int(c) for c in s.strip().split()]
       
    sL = list()
    for word in rL:
        sub = [SBox[n] for n in word]
        sL.append(sub)
    # ak.printHex(sL)
    rL = sL
    
    # step 3 is AddRoundKey
    rL = xorWordLists(rL, kL)
        
    # step 4 is InvMixColumns
    # we call out, and then skip in round 10
    if not last:
        rL = mixColumnsDecrypting(rL)
     
    return rL

#----------------------------------------

def doEncrypt(sched, input):
    initial_key = sched[:4]
    state = doRound0(initial_key, input)
    print "Encrypt"
    print "key:      ",
    ak.printHex(initial_key)
    print "data:     ",
    ak.printHex(input)
    
    # first 9 rounds the same
    for i in range(1,10):
        j = i*4
        kL = sched[j:j+4]
        result = doOneRoundEncrypt(state, kL)
        print "round " + str(i).rjust(2) + ": ",
        ak.printHex(result)
        state = result
    
    kL = sched[-4:]
    result = doOneRoundEncrypt(state, kL, last = True)
    print "round 10: ",
    ak.printHex(result)
    return result
    
def special_reverse(L):
    rL1 = L[40:] + L[36:40] + L[32:36] + L[28:32]
    rL2 = L[24:28] + L[20:24] + L[16:20] + L[12:16]
    rL3 = L[8:12] + L[4:8] + L[:4]
    return rL1 + rL2 + rL3
    
def doDecrypt(sched, input):
    # key schedule followed in reverse order
    # we need a special reverse
    initial_key = sched[-4:]
    state = input
        
    print "doDecrypt"
    print "key:      ",
    ak.printHex(initial_key)
    print "data:     ",
    ak.printHex(state)

    # first 9 rounds the same
    # we do not have the key as the first element
    # so we should start from 0!!
    for i in range(9):
        j = i*4
        kL = sched[j:j+4]
        result = doOneRoundDecrypt(state, kL)
        print "round " + str(i).rjust(2) + ": ",
        ak.printHex(result)
        state = result
    
    kL = sched[-4:]
    rL = doOneRoundDecrypt(state, kL, last = True)
    print "round 10: ",
    ak.printHex(rL)
    
    result = doRound0(initial_key, rL)
    print "final:    ",
    ak.printHex(result)
    return result

if __name__ == "__main__":
    # ultimately keys will be something like
    # [[0,1,2,3].. [12,13,14,15]]   
    key_string = 'Thats my Kung Fu'
    
    sched = getKeySchedule(key_string, mode='str')
    print "schedule:"
    print_schedule(sched)
   
    # msg.txt:  'Two One Nine Two'
    mL = getMessageWords('msg.txt')

    ctxt = doEncrypt(sched, mL)
    print "ciphertxt:",
    ak.printHex(ctxt)
    print
   
    sched = special_reverse(sched)
    #print "schedule:"
    #print_schedule(sched)
    doDecrypt(sched, ctxt)
   
   