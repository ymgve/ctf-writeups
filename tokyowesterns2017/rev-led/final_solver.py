import binascii, random

from notLED import notLED

enc = notLED()

def colordata_to_bits():
    s = ""
    for line in open("rawcolors.txt", "rb"):
        n = int(line.split()[2][:-1])
        if n <= 650000:
            s += "0"
        else:
            s += "1"
            
    prev = "0"
    prev_offset = 0
    res = []
    for i in xrange(len(s)):
        if s[i] != prev:
            res.append((prev, i - prev_offset))
            prev = s[i]
            prev_offset = i
            

    bits = ""
    for x, dist in res:
        i = int(dist / 7.5 + 0.5)
        bits += "0" * (i-1) + "1"
        
    return bits

bits = colordata_to_bits().strip("0")

# don't know how many zero bits are at the start of the sequence, so brute force
for offset in xrange(16):
    candbits = "0" * offset
    candbits += bits
    while len(candbits) % 64 != 0:
        candbits += "0"
        
    bytes = ""
    for i in xrange(0, len(candbits), 8):
        bytes += "%02x" % int(candbits[i:i+8], 2)
        
    # flip ciphertext nibbles
    fixed_bytes = bytes[0:48]
    for i in xrange(48, len(bytes), 2):
        fixed_bytes += bytes[i:i+2][::-1]
        
    K = fixed_bytes[0:32]
    
    res = ""
    for block in xrange(32, len(fixed_bytes)-16, 16):
        IV = fixed_bytes[block:block+16]
        CT = fixed_bytes[block+16:block+32]
        
        key1 = [[0 for x in range(4)] for x in range(4)]
        key2 = [[0 for x in range(4)] for x in range(4)]
        state = [[0 for x in range(4)] for x in range(4)]

        for y in xrange(4):
            for x in xrange(4):
                key1[y][x] = int(K[x+y*4], 16)

        for y in xrange(4):
            for x in xrange(4):
                key2[y][x] = int(K[16+x+y*4], 16)
                
        for y in xrange(4):
            for x in xrange(4):
                state[y][x] = int(CT[x+y*4], 16)

        state = enc.ledDecrypt128(state, key1, key2)

        for y in xrange(4):
            for x in xrange(4):
                state[y][x] ^= int(IV[x+y*4], 16)

        for y in xrange(4):
            for x in xrange(4):
                res += "%1x" % state[y][x^1]
                
    res = binascii.a2b_hex(res)
    if res.startswith("TWCTF"):
        print repr(res)
