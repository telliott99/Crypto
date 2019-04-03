from aes_utils import convert, printable
from aes_mix_columns import mix_one_column

D = { 'db 13 53 45' : '8e 4d a1 bc',
      'f2 0a 22 5c' : '9f dc 58 9d',
      '01 01 01 01' : '01 01 01 01',
      'c6 c6 c6 c6' : 'c6 c6 c6 c6',
      'd4 d4 d4 d5' : 'd5 d5 d7 d6',
      '2d 26 31 4c' : '4d 7e bd f8' }
    
def test():
    for k in D.keys():
        L = convert(k)
        result = mix_one_column(L)
        s = printable(result)
        print("%s -> %s" % (k,s))
        assert D[k] == s
 
test()
