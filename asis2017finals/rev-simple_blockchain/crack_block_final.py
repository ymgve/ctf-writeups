import hashlib

try:
    import psycox; psyco.full()
except ImportError:
    pass

ab = "*ASI{_7hiZ4bLoCkcaNmult0nrT!}" # optimized alphabet after flag was found

# ab = "*!abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"

def bruteforce_block0(prevhash):
    for d in ab:
        dd = d * 61
        for aa in ab:
            for bb in ab:
                for cc in ab:
                    cand = aa+bb+cc+dd
                    if hashlib.sha256(hashlib.sha256(cand).digest()).digest() == prevhash:
                        return cand
                        
def bruteforce_block(timestamp, prevhash, currhash):
    for d in ab:
        dd = d * 61
        for aa in ab:
            for bb in ab:
                for cc in ab:
                    cand = aa+bb+cc+dd
                    if hashlib.sha256(timestamp + prevhash + cand).digest() == currhash:
                        return cand
                        
f = open("block", "rb")

blocks = []
curr = {}
nxt = {}

while True:
    block = f.read(7 + 64 + 1)
    if len(block) == 0:
        break
        
    timestamp = block[0:7]
    prevhash = block[7:7+32]
    currhash = block[7+32:7+64]
    
    blocks.append((timestamp, prevhash, currhash))
    
    curr[currhash] = (timestamp, prevhash, currhash)
    nxt[prevhash] = (timestamp, prevhash, currhash)

currblock = blocks[0]
while currblock[1] in curr:
    currblock = curr[currblock[1]]
    
flag = ""

index = 0
while True:
    timestamp, prevhash, currhash = currblock
    
    if index == 0:
        data = bruteforce_block0(prevhash)
        flag += data[0:4]
    else:
        data = bruteforce_block(timestamp, prevhash, currhash)
        flag += data[0:4]

    print flag
    if currhash not in nxt:
        break
        
    currblock = nxt[currhash]
    index += 1
    
# *****************ASIS{_7hiS__iZ_4_bLoCkchaiN_Simul4ti0n_4rT!!!}*****************
