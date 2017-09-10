#!/usr/bin/python

import random
from secret import FLAG, KEY

def xor_str(x, y):
    print x
    print y
    if len(x) > len(y):
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x[:len(y)], y)])
    else:
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x, y[:len(x)])])

flag, key = FLAG.encode('hex'), KEY.encode('hex')

c = xor_str(key * (len(flag) // len(key) + 1), flag).encode('hex')
print c
enc = ''
for i in xrange(0, len(c), 2):
    r = random.randint(0, 15)
    enc += chr(int(hex(r)[-1] + hex(r ^ int(c[i+1], 16))[-1], 16))

print enc.encode("hex")

# ef = open('flag.enc', 'w')
# ef.write(enc)
# ef.close()