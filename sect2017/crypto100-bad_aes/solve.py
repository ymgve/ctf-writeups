import binascii, itertools

def xor(a, b):
    assert len(a) == len(b)
    s = ""
    for i in xrange(len(a)):
        s += chr(ord(a[i]) ^ ord(b[i]))
        
    return s
    
from aes import * # slightly modified from https://github.com/bozhu/AES-Python to support setting the Sbox

key = binascii.a2b_hex(open("key.txt", "rb").read().strip())
IV = binascii.a2b_hex(open("iv.txt", "rb").read().strip())
ct = open("text.enc", "rb").read()

sbox_partial = binascii.a2b_hex(open("sbox.txt", "rb").read().strip().replace("x", ""))

cands = []
for c in xrange(256):
    if chr(c) not in sbox_partial:
        cands.append(c)
        
for perm in itertools.permutations(cands):
    sbox = [ord(x) for x in sbox_partial]
    sbox.extend(perm)
    
    sbox_rev = [None] * 256
    for i in xrange(256):
        sbox_rev[sbox[i]] = i
        
    aesobj = AES(int(binascii.b2a_hex(key), 16), sbox, sbox_rev)
    
    res = aesobj.decrypt(int(binascii.b2a_hex(ct[0:16]), 16))
    res = binascii.a2b_hex("%032x" % res)
    res = xor(res, IV)
    
    count = 0
    for c in res:
        if ord(c) >= 32 and ord(c) <= 126:
            count += 1
            
    if count == 16:
        s = res
        
        for i in xrange(16, len(ct), 16):
            IV2 = ct[i-16:i]
            res = aesobj.decrypt(int(binascii.b2a_hex(ct[i:i+16]), 16))
            res = binascii.a2b_hex("%032x" % res)

            res = xor(res, IV2)
            s += res
            
        print repr(s)
            
        
        