import struct

tokens = {}
for line in open("basictokens.txt", "rb"):
    t, n = line.strip().split(" ")
    tokens[chr(int(t, 16))] = n.upper()
    
data = open("crackme.prg", "rb").read()

def hx(mem, idx):
    return mem[idx] + mem[idx+1] * 256
    
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
        
        s = ""
        idx = linestart + 4
        while True:
            c = chr(mem[idx])
            if c == "\x00":
                break
                
            if c in tokens:
                s += tokens[c]
            else:
                s += c
                
            idx += 1
                
        print "%04x %04x %d %s" % (linestart, nextline, linenumber, s)
        if nextline == 0:
            break
            
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
    
exit()
mem[3397] = 199
mem[3398] = 13

for i in xrange(3741, 4981+1):
    mem[i] = (mem[i] + 148) & 0xff

print_basic_program(mem)

mem[3397] = 29
mem[3398] = 20

for i in xrange(5363, 6632+1):
    mem[i] = (mem[i] + 152) & 0xff
    
print_basic_program(mem)

mem[3397] = 144
mem[3398] = 26

for i in xrange(7014, 8219+1):
    mem[i] = (mem[i] + 165) & 0xff
    
print_basic_program(mem)

mem[3397] = 195
mem[3398] = 32

for i in xrange(8601, 9868+1):
    mem[i] = (mem[i] + 184) & 0xff
    
print_basic_program(mem)

mem[3397] = 52
mem[3398] = 39

for i in xrange(10250, 11483+1):
    mem[i] = (mem[i] + 199) & 0xff
    
print_basic_program(mem)

mem[3397] = 131
mem[3398] = 45

for i in xrange(11865, 13107+1):
    mem[i] = (mem[i] + 240) & 0xff
    
print_basic_program(mem)

mem[3397] = 219
mem[3398] = 51

for i in xrange(13489, 14760+1):
    mem[i] = (mem[i] + 249) & 0xff
    
print_basic_program(mem)

mem[3397] = 80
mem[3398] = 58

for i in xrange(15142, 16351+1):
    mem[i] = (mem[i] + 132) & 0xff
    
print_basic_program(mem)

mem[3397] = 135
mem[3398] = 64

for i in xrange(16733, 17975+1):
    mem[i] = (mem[i] + 186) & 0xff
    
print_basic_program(mem)

mem[3397] = 223
mem[3398] = 70

for i in xrange(18360, 19633+1):
    mem[i] = (mem[i] + 214) & 0xff
    
print_basic_program(mem)

mem[3397] = 91
mem[3398] = 77

for i in xrange(20020, 21265+1):
    mem[i] = (mem[i] + 245) & 0xff
    
print_basic_program(mem)

mem[3397] = 187
mem[3398] = 83

for i in xrange(21652, 22923+1):
    mem[i] = (mem[i] + 203) & 0xff
    
print_basic_program(mem)

mem[3397] = 53
mem[3398] = 90

for i in xrange(23310, 24584+1):
    mem[i] = (mem[i] + 223) & 0xff
    
print_basic_program(mem)

mem[3397] = 178
mem[3398] = 96

for i in xrange(24971, 26178+1):
    mem[i] = (mem[i] + 237) & 0xff
    
print_basic_program(mem)

mem[3397] = 236
mem[3398] = 102

for i in xrange(26565, 27837+1):
    mem[i] = (mem[i] + 192) & 0xff
    
print_basic_program(mem)

mem[3397] = 103
mem[3398] = 109

for i in xrange(28224, 29471+1):
    mem[i] = (mem[i] + 157) & 0xff
    
print_basic_program(mem)

mem[3397] = 201
mem[3398] = 115

for i in xrange(29858, 31101+1):
    mem[i] = (mem[i] + 158) & 0xff
    
print_basic_program(mem)

mem[3397] = 39
mem[3398] = 122

for i in xrange(31488, 32761+1):
    mem[i] = (mem[i] + 235) & 0xff
    
print_basic_program(mem)

mem[3397] = 163
mem[3398] = 128

for i in xrange(33148, 34367+1):
    mem[i] = (mem[i] + 143) & 0xff
    
print_basic_program(mem)

mem[3397] = 239
mem[3398] = 134

print_basic_program(mem)
