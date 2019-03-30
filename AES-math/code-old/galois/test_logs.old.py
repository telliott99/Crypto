from GFlogs import exp_int, log_int

expL = [int(s) for s in exp_int.strip().split()]
logL = [int(s) for s in log_int.strip().split()]
logL.insert(0,None)

def test1(h1, h2):
    print "input hex:", h1, h2
    m = int('53',16)
    n = int('ca',16)
    print "input int: ", m, n
    
    x = logL[m]
    y = logL[n]
    print "logs:", x, y
    
    log_p = (logL[m] + logL[n]) % 256
    print "logp:", log_p
    
    p = expL[log_p]
    print hex(p)[2:].zfill(2)

# 0x53 x 0xca = 0x01
test1('53','ca')