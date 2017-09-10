#!/usr/bin/python

import random


KEY = 'musZTXmxV58UdwiKt8Tp'

def xor_str(x, y):
    if len(x) > len(y):
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x[:len(y)], y)])
    else:
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x, y[:len(x)])])

flag, key = open("flag.enc", "rb").read(), KEY.encode('hex')
enc = xor_str(key * (len(flag) // len(key) + 1), flag)

ef = open('flag.dec', 'wb')
ef.write(enc.decode('hex'))
ef.close()