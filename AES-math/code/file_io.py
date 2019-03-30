# no conversion to ints
def load_data(fn):
    with open(fn) as fh:
        data = fh.read()
    L = data.strip().split()
    L = [e.strip() for e in L]
    return L

def load_int_data(fn):
    L = load_data(fn)
    return [int(e) for e in L]

def write_data(s,fn):
    with open(fn,'w') as fh:
        fh.write(s + '\n')
    fh.close()


