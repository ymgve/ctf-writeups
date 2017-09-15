

disk = open("pwn.img", "rb").read()

s = ""
for c in disk[0x1400:0x1800]:
    s += chr(ord(c) ^ 0x13 ^ 0x37)
    
open("mysterycode.bin", "wb").write(s)
