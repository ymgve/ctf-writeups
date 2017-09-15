import struct

s = ""
s += struct.pack("<H", 0x1337 ^ 0x5275)
s += struct.pack("<H", 0x1337 ^ 0x5573)
s += struct.pack("<H", 0x3713 ^ 0x0723)
s += struct.pack("<H", 0x3713 ^ 0x7457)
s += struct.pack("<H", (0xAC23 - 0x1337) ^ 0xDEAD)
s += struct.pack("<H", (0xE9A5 + 0x1337) ^ 0xBEEF)
s += struct.pack("<H", (0xFCFF - 0x37 + 0x13) ^ 0xBEEF)
s += "3"

print repr(s)