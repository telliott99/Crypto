def string_division(b,d, v=True):
    if v:  print("string division")
    if v:  print(" " + b)  #why needed?
    n = len(d)
    pad = ""
    while len(b) >= n:
        i = 0
        while b[i] == d[i] and i < (n-1):
            i += 1
            
        # first i chars match, XOR what's left
        r = ''
        for j in range(i,n):
            if b[j] == d[j]:
                r = r + '0'
            else:
                r = r + '1'
        
        pad = pad + " " * i
        if v:  print(pad + d)
        # print(" " * i + r)
        b = r + b[n:]
        if v:  print(pad + " " * i + b)
        
        # strip leading 0's
        i = b.find('1')
        if i == -1:
            return '0'
        b = b[i:]
        pad = pad + " " * i
            
    return b

b = '100011011'
L = ['10','11',
     '111',
     '1011','1101',
     '10011', '11001', '11101', '11111']

def demo():
    for d in L:
        r = string_division(b,d)
        print('result:  %s\n' % r)

demo()

pL = list()

for i in range(256):
    b = '1' + bin(i)[2:].zfill(8)
    candidate = True
    for d in L:
        r = string_division(b,d, v=False)
        #print(r)
        if r == '0':
            candidate = False
    if candidate:
        pL.append(b)

print("found %d candidates" % len(pL))
print("\n".join(pL))
        