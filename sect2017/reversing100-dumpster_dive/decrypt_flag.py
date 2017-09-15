import binascii, struct

from Crypto.Cipher import AES

m30 = 0x9BF3EAD2 ^ 0x27A99754
m34 = 0xD302A721 ^ 0x3DCB1D90
m38 = 0x89AAFAE9 ^ 0xB1C15412
m3c = 0x50B0F029 ^ 0x1BCD5DFE

key = struct.pack("<IIII", m30, m34, m38, m3c)
a = AES.new(key, AES.MODE_ECB)

data = open("chall.bin", "rb").read() 

flag = ""
address = 0x000023C0 - 0x1000
while "}" not in flag:
    ct = data[address:address+16]

    flag += a.decrypt(ct)
    address += 16

print repr(flag)