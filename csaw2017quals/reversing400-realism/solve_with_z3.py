from z3 import *

def diff_func(a, b):
    return If(a > b, a - b, b - a)
    
bytes = []
for i in xrange(16):
    bytes.append(BitVec("byte%02d" % i, 16))
    
mask = (0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
        0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
        0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01)

results = (0x270, 0x211, 0x255, 0x229, 0x291, 0x25E, 0x233, 0x1F9, 0x278, 0x27B, 0x221, 0x209, 0x25D, 0x290, 0x28F, 0x2DF)

diff = []
for i in xrange(7):
    t = [0] * 16
    t[0] = results[i*2+3] & 0xff
    t[1] = results[i*2+3] >> 8
    t[8] = results[i*2+2] & 0xff
    t[9] = results[i*2+2] >> 8
    diff.append(t)
    
diff.append((0xb8, 0x13, 0x0, 0xcd, 0x10, 0xf, 0x20, 0xc0, 0x83, 0xe0, 0xfb, 0x83, 0xc8, 0x2, 0xf, 0x22))


s = Solver()

for sp in range(7, 0, -1):
    newbytes = []
    newbytes.extend(bytes[8:12])
    newbytes.extend(bytes[12:16])
    newbytes.extend(bytes[4:8])
    newbytes.extend(bytes[0:4])
    
    for i in xrange(16):
        newbytes[i] = newbytes[i] * mask[sp+1+i]
        
    n1 = 0
    for i in xrange(8):
        n1 += diff_func(newbytes[i], diff[sp][i])

    n2 = 0
    for i in xrange(8):
        n2 += diff_func(newbytes[i+8], diff[sp][i+8])
    
    s.add(n1 == results[sp*2+1])
    s.add(n2 == results[sp*2])

ab = []
for i in xrange(256):
    if chr(i) not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_":
        ab.append(i)
        
for i in xrange(16):
    s.add(bytes[i] < 256)
    s.add(bytes[i] >= 0)
    
    for c in ab:
        s.add(bytes[i] != c)
    
print s.check()
m = s.model()

res = ""
for i in xrange(16):
    res += chr(int(str(m[bytes[i]])))
    
print repr("flag" + res)

    