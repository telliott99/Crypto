from gmath import gmultiply

fwd = [
[2, 3, 1, 1],
[1, 2, 3, 1],
[1, 1, 2, 3],
[3, 1, 1, 2] ]

rev = [
[14, 11, 13,  9],
[ 9, 14, 11, 13],
[13,  9, 14, 11],
[11, 13,  9, 14] ]


def xor_word(w):
    r = 0
    for n in w:
        r = r ^ n
    return r

# w consists of 4 hex values
def mmult(w, reverse=False):
    L = [int(h,base=16) for h in w]
    rL = list()
    if reverse:
        a = rev
    else:
        a = fwd
    for row in a:
        r = [gmultiply(x,y) for x,y in zip(row,L)]
        rL.append(xor_word(r))
    return [hex(n)[2:].zfill(2) for n in rL]

def test_matrix(w = ['db','13','53','45']):
    print(w)
    r = mmult(w)
    print(r)
    b = mmult(r, reverse=True)
    print(b)

test_matrix()

'''
['db', '13', '53', '45']
['8e', '4d', 'a1', 'bc']
['db', '13', '53', '45']
'''