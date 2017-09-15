import struct, binascii

from Crypto.Cipher import DES3
from Crypto.Cipher import AES

from sha256 import * # from https://github.com/thomdixon/pysha2/blob/master/sha2/sha256.py
        
hash0, hash1, hash2, hash3 = (0x37833c82aec93c6d, 0x668592081ed67c95, 0x2219c1888c430c17, 0x77aebde7e52e924f)

aeskey0, aeskey1, aeskey2, aeskey3 = (0x3e434b0b0aa93bb2, 0x82b03e164d85ce2a, 0x845d334203640aee, 0x2011a08bd4310e26)

# encrypted data from server
serverdata = binascii.a2b_hex("9095410de22a3275db680010ba0c9942e28a84ca1264f2a222529d7d992e67fba149bb634882b48495bd783c6852d132b637c0d9413969518fbcfd5823e545c7")
cr = AES.new(struct.pack(">QQQQ", aeskey0, aeskey1, aeskey2, aeskey3), AES.MODE_ECB)
keydata = cr.decrypt(serverdata)

# keydata goes through one internal round of SHA256 but initial values are nonstandard
h = sha256()
h._h = (hash0 >> 32, hash0 & 0xffffffff, hash1 >> 32, hash1 & 0xffffffff, hash2 >> 32, hash2 & 0xffffffff, hash3 >> 32, hash3 & 0xffffffff)
h._sha256_process(keydata)

# decrypt creds.txt file
iv0, iv1 = (0xb6fa1d15ed46055d, 0x96e7f1e8cb561781)
ct = open("creds.txt", "rb").read()
cr = AES.new(struct.pack(">IIIIIIII", h._h[0], h._h[1], h._h[2], h._h[3], h._h[4], h._h[5], h._h[6], h._h[7]), AES.MODE_CBC, struct.pack(">QQ", iv0, iv1))
print cr.decrypt(ct)

# decrypt hacked message with 3DES
key0, key1, key2, iv = (0x6011b396042a187a, 0xafebe6d990f0c393, 0x7e7b44705a7100e1, 0x92097f6e08112274)
data = open("a.out", "rb").read()
ct = data[0x2010:0x2e38]
cr = DES3.new(struct.pack(">QQQ", key0, key1, key2), DES3.MODE_CBC, struct.pack(">Q", iv))

print cr.decrypt(ct)

# SECT{C0M3_S41L_7H3_5345_W17H_0UR_74NK3R5!}