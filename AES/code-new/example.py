import sys, random
from aes_encrypt import encrypt
from aes_decrypt import decrypt

try:
    p = sys.argv[1]
except IndexError:
    p = "Two One Nine Two"
    
SZ = 16 
p = p[:SZ]
if len(p) < SZ:
    x = SZ - len(p)
    p += "X" * x
    
#-------------------
    
try:
    k = sys.argv[2]
except IndexError:
    k = "Thats my Kung Fu"
    
k = k[:SZ]

s = 'abcdefghijklmnopqrstuvwxyz'
s += '0123456789'

while len(k) < SZ: 
    k += random.choice(s)

print("Key was too short so I added some more.")
    
#-------------------
# p = "strawberryfields"
hex_ctx = encrypt(k,p)
result = decrypt(k,hex_ctx)
print(''.join([chr(n) for n in result]))
