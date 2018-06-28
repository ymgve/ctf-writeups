import struct, hashlib

from Crypto.Cipher import AES

class RNG(object):
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66DL) & ((1L << 48) - 1)
        
    def nextint(self):
        self.seed = (self.seed * 0x5DEECE66DL + 0xBL) & ((1L << 48) - 1)
        x = (self.seed >> 16) & 0xffffffff
        return x
        
rng = RNG(((((((((1416127776 + 1869507705) + 544696686) + 1852403303) + 544042870) + 1696622963) + 544108404) + 544501536) + 1886151033))

s = ""
for i in xrange(8):
    x = rng.nextint()
    s += struct.pack("<I", x)

ct = "".join(chr(x & 0xff) for x in (-61, 15, 25, -115, -46, -11, 65, -3, 34, 93, -39, 98, 123, 17, 42, -121, 60, 40, -60, -112, 77, 111, 34, 14, -31, -4, -7, 66, 116, 108, 114, -122))

for i in xrange(1000000):
    s = hashlib.sha256(s).digest()
    
res = AES.new(s, AES.MODE_ECB).decrypt(ct)

print repr(res)
