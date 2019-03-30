from gdict import logD, antilogD
from file_io import write_data

# the log of 1 is zero, write it explicitly
rL = ["1,1"]

for i in range(2,256):
    log_i = logD[i]
    log_j = 255 - log_i
    mi = antilogD[log_j]
    rL.append("%d,%d" % (i,mi))
    
s = '\n'.join(rL)
write_data(s,"mi.txt")
    
'''
# the result is list of tuples
1,1
2,141
3,246
..
'''