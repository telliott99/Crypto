# python aes128_ebc.py > aes128_ecb.output.txt

# byte is just an int
# an aes word is a list of 4 bytes
# an aes block or key is a list of 4 words

# key schedule is a flat list of 44 words 
# first schedule[:4] is the initial key

import sys
import aes_utils as ut
import aes_info, aes_matrix
import aes_key as ak
import aes_core

SZ = 16

def doEncrypt(sched, input, verbose = True):
    v = verbose
    if v:  print "\nEncrypt"
    if v:  print "input:    ",
    if v:  ak.printHex(input)
    
    initial_key = sched[:4]
    state = aes_core.doRound0(initial_key, input)
    if v:  print "\nkey:      ",
    if v:  ak.printHex(initial_key)
    
    # print "data:     ",
    # ak.printHex(state)
    
    # first 9 rounds the same
    for i in range(1,10):
        j = i*4
        kL = sched[j:j+4]
        result = aes_core.doOneRoundEncrypt(state, kL)
        if v:  print "round " + str(i).rjust(2) + ": ",
        if v:  ak.printHex(result)
        state = result
    
    kL = sched[-4:]
    result = aes_core.doOneRoundEncrypt(state, kL, last = True)
    if v:  print "round 10: ",
    if v:  ak.printHex(result)
    return result
    
def special_reverse(L, n=4):
    LEN = len(L)
    assert LEN % n == 0
    
    rL = list()
    for j in range(LEN,0,-4): 
        i = j - 4
        rL.extend(L[i:j])
    return rL
    
    #rL1 = L[40:] + L[36:40] + L[32:36] + L[28:32]
    #rL2 = L[24:28] + L[20:24] + L[16:20] + L[12:16]
    #rL3 = L[8:12] + L[4:8] + L[:4]
    #return rL1 + rL2 + rL3
    
def doDecrypt(sched, input, verbose = True):
    v = verbose
    if v:  print "\nDecrypt"
    if v:  print "input:    ",
    if v:  ak.printHex(input)
    
    state = input

    # AddRoundKey comes first before SubBytes, etc.
    kL = sched[0:4]
    state = aes_core.doRound0(kL, state)
        
    if v:  print "\nkey:      ",
    initial_key = sched[-4:]
    if v:  ak.printHex(initial_key)

    # first 9 rounds the same
    # we do not have the key as the first element
    # so we should start from 0!!
    for i in range(9):
        j = i*4 + 4
        kL = sched[j:j+4]
        result = aes_core.doOneRoundDecrypt(state, kL)
        if v:  print "round " + str(i + 1).rjust(2) + ": ",
        if v:  ak.printHex(result)
        state = result
    
    kL = sched[-4:]
    rL = aes_core.doOneRoundDecrypt(state, kL, last = True)
    if v:  print "round 10: ",
    if v:  ak.printHex(rL)
    
    if v:  print "final:    ",
    if v:  ak.printHex(rL)
    return rL

def aes_ecb(schedule, msg_filename, verbose = True):  
    v = verbose
    #sched = ak.getKeySchedule(key_string, mode='str')
    if v:  print "key schedule:"
    if v:  ak.print_schedule(schedule)
   
    # msg.txt:  'Two One Nine Two'
    mL = ut.getMessageWords(msg_filename)

    ctxt = doEncrypt(schedule, mL, verbose = True)
    if v:  print "ciphertxt:",
    if v:  ak.printHex(ctxt)
    if v:  print
   
    # key schedule followed in reverse order
    # we need a special reverse
    schedule = special_reverse(schedule)
    return doDecrypt(schedule, ctxt, verbose = True)

if __name__ == "__main__":
    # ultimately keys will be something like
    # [[0,1,2,3].. [12,13,14,15]]   
    key_string = 'Thats my Kung Fu'
    schedule = ak.getKeySchedule(key_string, mode='str')
    aes_ecb(schedule, 'msg.txt')
