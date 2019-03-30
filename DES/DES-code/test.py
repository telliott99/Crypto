from pydes import des

key = '133457799BBCDFF1'
msg = '0123456789abcdef'

ctx = des(msg,key)
print(ctx)
assert ctx == '85e813540f0ab405'

ptx = des(ctx,key,mode="decrypt")
print(ptx)
assert ptx == '0123456789abcdef'
