import aes_key_expand
import aes_utils as ut
import fmt

# from fips
k = '2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c'
k = ut.convert(k)

kL = aes_key_expand.get_keys(k)
for k in kL:
    print(ut.printable(k))
    
w = kL[-1][-4:]
ut.printable(w) == 'b6 63 0c a6'   # from fips


'''
> python test_key_expansion.py 
2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c
a0 fa fe 17 88 54 2c b1 23 a3 39 39 2a 6c 76 05
f2 c2 95 f2 7a 96 b9 43 59 35 80 7a 73 59 f6 7f
3d 80 47 7d 47 16 fe 3e 1e 23 7e 44 6d 7a 88 3b
ef 44 a5 41 a8 52 5b 7f b6 71 25 3b db 0b ad 00
d4 d1 c6 f8 7c 83 9d 87 ca f2 b8 bc 11 f9 15 bc
6d 88 a3 7a 11 0b 3e fd db f9 86 41 ca 00 93 fd
4e 54 f7 0e 5f 5f c9 f3 84 a6 4f b2 4e a6 dc 4f
ea d2 73 21 b5 8d ba d2 31 2b f5 60 7f 8d 29 2f
ac 77 66 f3 19 fa dc 21 28 d1 29 41 57 5c 00 6e
d0 14 f9 a8 c9 ee 25 89 e1 3f 0c c8 b6 63 0c a6
> 
'''
