from pyaes import aes_ecb as ecb
from pyaes import aes_key as ak


key_string = 'Thats my Kung Fu'
schedule = ak.getKeySchedule(key_string, mode='str')
ecb(schedule, 'msg.txt')
