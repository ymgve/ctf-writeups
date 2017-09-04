import binascii

leet_table = open("leet_table", "rb").read()
elf_table = open("cryptal", "rb").read()

def swap_bits(bits, index, multval, switchflag):
    if switchflag == 1:
        modval = (index + multval) % len(bits)
    else:
        modval = (index - multval) % len(bits)
        
    bits[index], bits[modval] = bits[modval], bits[index]
    
def swap_bytes(bits, index, multval, switchflag):
    if switchflag == 1:
        modval = (index + multval) % (len(bits) / 8)
    else:
        modval = (index - multval) % (len(bits) / 8)
        
    bits[index*8:index*8+8], bits[modval*8:modval*8+8] = bits[modval*8:modval*8+8], bits[index*8:index*8+8]
        
bits = []
for i in xrange(8025*8):
    bits.append(str(i))
    
for round in xrange(0x20):
    leetindex = 0
    elfindex = 0
    for i in xrange(len(bits)):
        mult = ord(leet_table[leetindex]) * ord(elf_table[elfindex])
        
        if bits[i][0] == "!":
            bits[i] = bits[i][1:]
        else:
            bits[i] = "!" + bits[i]
        
        swap_bits(bits, i, mult, i & 1)
        
        elfindex += 1
        if elfindex >= len(elf_table):
            elfindex = 0
            
        leetindex += 1
        if leetindex >= len(leet_table):
            leetindex = 0
            
    leetindex = 0
    elfindex = 0
    for i in xrange(len(bits)/ 8):
        mult = ord(leet_table[leetindex]) * ord(elf_table[elfindex])
        
        swap_bytes(bits, i, mult, i & 1)
        
        elfindex += 1
        if elfindex >= len(elf_table):
            elfindex = 0
            
        leetindex += 1
        if leetindex >= len(leet_table):
            leetindex = 0
            
data = open("flag.png.enc", "rb").read()

bitdata = []
for c in data:
    for i in xrange(8):
        bitdata.append((ord(c) >> i) & 1)
        
result = [0] * len(bits)
for i in xrange(len(bits)):
    if bits[i][0] == "!":
        n = int(bits[i][1:])
        result[n] = bitdata[i] ^ 1
    else:
        n = int(bits[i])
        result[n] = bitdata[i]
        
bytes = []
for i in xrange(0, len(result), 8):
    t = "".join(str(x) for x in result[i:i+8][::-1])
    bytes.append(int(t, 2))

s = "".join(chr(x) for x in bytes)
open("decrypted.png", "wb").write(s)
