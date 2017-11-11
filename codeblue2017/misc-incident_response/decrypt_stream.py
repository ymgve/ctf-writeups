import binascii

from Crypto.Cipher import ARC4

key = binascii.a2b_hex("b0f870fb7587c0482bb7f7c1f7391f9e66de2cd92558ca1f87f2df232fedc7da")

c = ARC4.new(key)

for line in open("stream.txt", "rb"):
    ct = binascii.a2b_hex(line.strip())
    print c.decrypt(ct)
