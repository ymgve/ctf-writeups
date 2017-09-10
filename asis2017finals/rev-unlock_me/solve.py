
intmax = 0xffffffff

def ror(v, n):
    return (v >> n) | ((v << (32-n)) & intmax)

def op1(a, b, c):
    a ^= intmax
    c |= 0x8FD6F5D4
    a = ror(a, 10)
    b = ror(b, 4)
    b ^= 0x30BE77F2
    c ^= intmax
    c &= 0xF5A4C061
    c &= 0x259A904C
    c ^= 0x9A1097C4
    a = ror(a, 24)
    return a, b, c
    
def op2(a, b, c):
    c = (c + 0xB58B95F8) & intmax
    b |= 0x4A61F1CE
    c ^= intmax
    a = ror(a, 5)
    b |= 0xDF0725C3
    b = (b + 0x35A19CFD) & intmax
    c = (c + 0xEC3A12E6) & intmax
    a = (a + 0x49D48C03) & intmax
    b = ror(b, 8)
    a ^= intmax
    return a, b, c
    
def op3(a, b, c):
    a ^= intmax
    b = (b + 0xF630866C) & intmax
    a = (a + 0x86A5904A) & intmax
    a = (a + 0xDC60B97D) & intmax
    b = ror(b, 17)
    c ^= 0xA6738F46
    c = ror(c, 17)
    b = (b + 0x28F369D9) & intmax
    c ^= intmax
    c = ror(c, 12)
    return a, b, c
    
def op4(a, b, c):
    b = (b + 0x66A0F372) & intmax
    b = ror(b, 6)
    b = ror(b, 18)
    a |= 0x57D6409D
    b = ror(b, 5)
    b = ror(b, 10)
    b &= 0x957E59B7
    c &= 0xA977CB85
    c ^= intmax
    b ^= 0xD0DA41C9
    return a, b, c
    
def op5(a, b, c):
    b ^= intmax
    a &= 0x39DE8AF2
    a |= 0xC3158744
    c = ror(c, 29)
    b = ror(b, 14)
    b = ror(b, 6)
    a |= 0x5003210A
    c ^= intmax
    b ^= intmax
    b ^= 0x5A8ED70
    return a, b, c
    
funcs = (op1, op2, op3, op4, op5)

def recurse(sofar, abc):
    (a, b, c) = abc
    if len(sofar) == 10:
        if a == 0xD7DFEFFF and b == 0x50A001E9 and c == 0xD68CBE7F:
            print hex(a), hex(b), hex(c), sofar
    else:
        for i in xrange(5):
            recurse(sofar + str(i+1), funcs[i](a, b, c))
            
recurse("", (0x12345, 0xA9867, 0xFEDCB))