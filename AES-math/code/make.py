from fmt import fmt
from file_io import write_data
from gmath import gmultiply as gm

def make_powers(gen):
    r = 1
    L = [r]
    for i in range(255):
        r = gm(r, gen)
        L.append(r)
    return L
    
def make_logs(powers):
    D = dict()
    for i,n in enumerate(powers[:255]):
        D[n] = i
    # no 0 present
    return [D[j] for j in list(range(1,256))]


def do_all(gen):
    L = make_powers(gen)
    s = fmt(L)
    write_data(s, 'g' + str(gen) + '.powers.int.txt')
    s = fmt(L, hex_fmt=True)
    write_data(s, 'g' + str(gen) + '.powers.hex.txt')
    
    inputL = L[:]
    L = make_logs(inputL)
    s = fmt(L, skip_first=True)
    write_data(s, 'g' + str(gen) + '.logs.int.txt')
    s = fmt(L, hex_fmt=True, skip_first=True)
    write_data(s, 'g' + str(gen) + '.logs.hex.txt')

if __name__ == "__main__":
    do_all(3)