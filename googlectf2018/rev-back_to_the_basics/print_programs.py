import struct

def hx(mem, idx):
    return mem[idx] + mem[idx+1] * 256

tokens = {}
for line in open("basictokens.txt", "rb"):
    t, n = line.strip().split(" ")
    tokens[int(t, 16)] = n.upper()
    
data = open("crackme.prg", "rb").read()

mem = [0] * 0x10000
addr = struct.unpack("<H", data[0:2])[0]

for c in data[2:]:
    mem[addr] = ord(c)
    addr += 1

def print_basic_program(mem):
    print
    print "-----------------------------"
    print

    linestart = 0x0801
    while True:
        nextline = hx(mem, linestart)
        linenumber = hx(mem, linestart + 2)

        if nextline == 0:
            break
        
        s = ""
        idx = linestart + 4
        while True:
            b = mem[idx]
            if b == 0:
                break
                
            if b in tokens:
                s += tokens[b]
            else:
                s += chr(b)
                
            idx += 1
                
        print "%04x %04x %d %s" % (linestart, nextline, linenumber, s)
            
        linestart = nextline


lobytes = (199,  29, 144, 195,  52, 131, 219,  80, 135, 223,  91, 187,  53, 178, 236, 103, 201,  39, 163, 239)
hibytes = ( 13,  20,  26,  32,  39,  45,  51,  58,  64,  70,  77,  83,  90,  96, 102, 109, 115, 122, 128, 134)

starts = ( 3741,  5363,  7014,  8601, 10250, 11865, 13489, 15142, 16733, 18360, 20020, 21652, 23310, 24971, 26565, 28224, 29858, 31488, 33148)
ends   = ( 4981,  6632,  8219,  9868, 11483, 13107, 14760, 16351, 17975, 19633, 21265, 22923, 24584, 26178, 27837, 29471, 31101, 32761, 34367)

obfus = (148, 152, 165, 184, 199, 240, 249, 132, 186, 214, 245, 203, 223, 237, 192, 157, 158, 235, 143)

print_basic_program(mem)

for i in xrange(20):
    mem[3397] = lobytes[i]
    mem[3398] = hibytes[i]
    
    if i != 19:
        for j in xrange(starts[i], ends[i]+1):
            mem[j] = (mem[j] + obfus[i]) & 0xff

    print_basic_program(mem)
