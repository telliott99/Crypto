from aes_info import SE

round_const = [1, 2, 4, 8, 16, 
              32, 64, 128, 27, 54]

sL = [int(e) for e in SE.strip().split()]

#-----------------------------------------------

def wordXOR(L1,L2):
    ret = [a^b for a,b in zip(L1,L2)]
    return ret

def doRound(n,kL):
    w0 = kL[:4]
    w1 = kL[4:8]
    w2 = kL[8:12]
    w3 = kL[12:]

    # byte shift
    tmp = w3[1:] + w3[:1]

    # S box
    tmp = [sL[i] for i in tmp]
    
    # XOR
    tmp[0] = tmp[0] ^ round_const[n]

    w4 = wordXOR(w0,tmp)
    w5 = wordXOR(w4,w1)
    w6 = wordXOR(w5,w2)
    w7 = wordXOR(w6,w3)    
    ret = w4 + w5 + w6 + w7
    return ret
    
def doRounds(kL):
    rL = [kL[:]]
    for i in range(10):
        result = doRound(i,kL)
        rL.append(result[:])
        kL = result
    return rL

def get_keys(L):
    # print('s: %s' % s)
    # kL = [ord(c) for c in s]
    # print ' '.join([str(c).rjust(2) for c in kL])
    return doRounds(L)

if __name__ == "__main__":
    s = 'Thats my Kung Fu'
    L = [ord(c) for c in s]
    kL = get_keys(L)
    for line in kL:
        print(' '.join([str(i).rjust(3) for i in line]))

    for line in kL:
        print(' '.join([hex(i)[2:].zfill(2) for i in line]))
