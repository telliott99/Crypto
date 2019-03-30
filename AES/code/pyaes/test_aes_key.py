import aes_utils as ut
import aes_key

def testGetKeySchedule():
    s =  '00 00 00 00 00 00 00 00 '
    s += '00 00 00 00 00 00 00 00'
    schedule = aes_key.getKeySchedule(s, mode = 'hex')
    # ak.printHex(schedule[-4:])

#------------------------------

def ex1():
    key = 'hello'
    key = aes_key.padKey(key, padChar = '0')
    kL = aes_key.processTextKey(key)
    return ut.chunks(kL,4)

def ex2():
    return ut.chunks(range(16),4)
    
def ex3():
    key_schedule = [[15,21,113,201],
                    [71,217,232,89],
                    [12,183,173,214],
                    [175,127,103,152]]
    return key_schedule

def ex4():
    key = 'Thats my Kung Fu'
    kL = [ord(c) for c in key]
    return ut.chunks(kL,4)

def ex5():
    key_schedule = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
    return key_schedule

def ex6():
    input = [
        '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00',
        'ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff',
        '00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f',
        '69 20 e2 99 a5 20 2a 6d 65 6e 63 68 69 74 6f 2a']
        
    for s in input:
        k = [int(h,16) for h in s.strip().split()]
        kL = ut.chunks(k,4)
        L = aes_key.expand_key(10, kL)
        aes_key.printHex(L[:4] + L[-4:])
        print

def do_example(ex):
    key_schedule = ex()       
    L = aes_key.expand_key(10, key_schedule)
    aes_key.print_schedule(L)
    
if __name__ == "__main__":
    print "example 6"
    ex6()
    print "example 4"
    do_example(ex4)

    L = aes_key.expand_key(10, ex1())
    print "example 1"
    for i,word in enumerate(L):
        if i and i % 4 == 0:
            print
        print word
