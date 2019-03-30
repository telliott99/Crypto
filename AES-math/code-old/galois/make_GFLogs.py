# this is code to generate a table of powers 
# of the generator '0x03' for the field GF(2^8)

# to multiply by 3 = '0x03'
# multiply by '0x02' and then XOR with self        

# > python make_GFlogs.py > GFlogs.py

def times2(n):
    x2 = n * 2
    if x2 > 255:
        x2 = ((x2 % 256) ^ 27)
    return x2
    
def times3(n):
    x2 = times2(n)
    x3 = x2 ^ n
    return x3

def field_generator():
    n = 1
    while True:
        yield n
        n = times3(n)

#----------------------------------

def getHex(n):
    return hex(n)[2:].zfill(2)

def printTable(L, mode = 'int'):
    for row in range(16):
        i = row * 16
        j = i + 16
        sL = L[i:j]
        
        printing_logs = sL[0] == None
        if printing_logs:
            sL.pop(0)
        if mode == 'hex':
            pL = [getHex(n) for n in sL]
        else:
            pL = [str(n).rjust(3) for n in sL]
            
        if printing_logs and mode == 'hex':
            print '  ',
        if printing_logs and mode == 'int':
            print '   ',
            
        print ' '.join(pL)

#----------------------------------

# create list of the powers of 3
# computed by our special field arithmetic

# these are "exponents"
g = field_generator()
expL = [g.next() for i in range(256)]
print "exp_hex = " + "'''"
printTable(expL, mode = 'hex')
print "'''\n"
print "exp_int = " + "'''"
printTable(expL, mode = 'int')
print "'''\n"
 
# reverse expL to make table of logarithms
# logL[0] == None
logL = [None] * 256
for i in range(256):
    j = expL[i]
    logL[j] = i

print "log_hex = " + "'''"
printTable(logL, mode = 'hex')
print "'''\n"
print "log_int = " + "'''"
printTable(logL, mode = 'int')
print "'''\n"







