from Crypto.Cipher import AES
import os

def f(L):
    hL = [hex(ord(c))[2:].zfill(2) for c in L]
    return ''.join(hL)
    
key = os.urandom(16)
iv = os.urandom(16)
print ' k', f(key)
print 'iv', f(iv)

cipher = AES.new(key, AES.MODE_CTR, 
                 counter = lambda: iv)

s = 'aaa'
print ' s', s

ctx = cipher.encrypt(s)
print ' c', f(ctx)
print ' p', f(cipher.decrypt(ctx))
