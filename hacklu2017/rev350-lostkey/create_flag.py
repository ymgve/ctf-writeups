import struct, hashlib

def tea_decrypt(v, k):
    v0, v1 = v
    sum = 0xc6ef3720
    delta = 0x9e3779b9
    for i in xrange(32):
        t = ((v0 << 4) + k[2]) & 0xffffffff
        t ^= (v0 + sum) & 0xffffffff
        t ^= ((v0 >> 5) + k[3]) & 0xffffffff
        v1 = (v1 - t) & 0xffffffff
        
        t = ((v1 << 4) + k[0]) & 0xffffffff
        t ^= (v1 + sum) & 0xffffffff
        t ^= ((v1 >> 5) + k[1]) & 0xffffffff
        v0 = (v0 - t) & 0xffffffff
        
        sum = (sum - delta) & 0xffffffff
        
    return v0, v1
        
def tea_encrypt(v, k):
    v0, v1 = v
    sum = 0
    delta = 0x9e3779b9
    for i in xrange(32):
        sum = (sum + delta) & 0xffffffff
        t = ((v1 << 4) + k[0]) & 0xffffffff
        t ^= (v1 + sum) & 0xffffffff
        t ^= ((v1 >> 5) + k[1]) & 0xffffffff
        v0 = (v0 + t) & 0xffffffff
        
        t = ((v0 << 4) + k[2]) & 0xffffffff
        t ^= (v0 + sum) & 0xffffffff
        t ^= ((v0 >> 5) + k[3]) & 0xffffffff
        v1 = (v1 + t) & 0xffffffff
        
    return v0, v1
    
def get_argv1():
    argv1 = struct.pack("<I", 0x466C7578 ^ 0x210D191E) + struct.pack("<I", 0x78756C46 ^ 0x4B1D383D)
    return argv1

def get_argv2():
    s = ""
    for n in (0x37d02c61, 0x63979f3b, 0xd07e4607, 0xad79934a, 0xddbdbbca, 0x64a669e7, 0x00000068):
        s += struct.pack("<I", n)
     
    s = s.rstrip("\x00")

    res = ""
    t = 65
    for c in s[::-1]:
        n = ord(c) ^ t
        n = ((n >> 4) | (n << 4)) & 0xff
        n ^= 0xff
        res += chr(n)
        t = n
        
    argv2 = res[::-1]
    return argv2
    
def get_argv3():
    argv3 = "p4rtme"
    assert hashlib.md5(argv3).hexdigest() == "7b4d6ff46ac46c3f628acc930d937d81"

    return argv3

def get_argv4():
    k = 0xc2e1faff, 0xfffae1c2, 0xfffae1c2, 0xc2e1faff
    argv4 = ""
    
    v = 0xa42d6ebf, 0xefe89e7
    v = tea_decrypt(v, k)
    argv4 += struct.pack("<II", v[0], v[1])

    v = 0xaadd934d, 0x4e4e7f13
    v = tea_decrypt(v, k)
    argv4 += struct.pack("<II", v[0], v[1])

    v = 0x8ec32ca9, 0x8559d4e9
    v = tea_decrypt(v, k)
    argv4 += struct.pack("<II", v[0], v[1])

    return argv4

print repr(get_argv1() + get_argv2() + get_argv3() + get_argv4())
