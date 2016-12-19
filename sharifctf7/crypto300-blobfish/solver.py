from hashlib import md5

s = [59, 21, 25, 32, 30, 3, 63, 38, 5, 29, 40, 53, 17, 56, 58, 37, 45, 43, 52, 61, 7, 55, 57, 12, 26, 13, 49, 16, 36, 8, 31, 41, 20, 51, 33, 15, 1, 0, 23, 27, 35, 18, 47, 62, 14, 60, 10, 54, 46, 50, 9, 48, 24, 28, 44, 2, 6, 34, 19, 42, 11, 39, 22, 4]
p = [14, 7, 25, 2, 22, 32, 29, 0, 28, 31, 6, 18, 12, 27, 33, 9, 17, 21, 8, 26, 23, 35, 4, 5, 11, 20, 30, 24, 15, 1, 19, 16, 10, 13, 34, 3]

rounds = 3
nsbox = 6   # number of s-boxes
bsbox = 6   # input bits per s-box
ssize = 1 << bsbox
bits = nsbox * bsbox
insize = 1 << bits

#####################################################
import sys

#####################################################

try:
    import psyco; psyco.full()
except ImportError:
    pass

_s_inv = [0] * len(s)
for i in range(len(s)):
	_s_inv[s[i]] = i

_p_inv = [0] * len(p)
for i in range(len(p)):
	_p_inv[p[i]] = i

def sbox(x):
    return s[x]

def pbox(x):
    y = 0
    for i in range(len(p)):
        y |= ((x >> i) & 1) << p[i]
    return y

def inv_s(x):
	return _s_inv[x]

def inv_p(x):
	y = 0
	for i in range(len(p)):
		y |= ((x >> p[i]) & 1) << i
	return y

def split(x):
    y = [0] * nsbox
    for i in range(nsbox):
        y[i] = (x >> (i * bsbox)) & 0x3f
    return y

def merge(x):
    y = 0
    for i in range(nsbox):
        y |= x[i] << (i * bsbox)
    return y

def roundd(p, k):
    u = [0] * nsbox
    x = split(p)
    for i in range(nsbox):
        u[i] = sbox(x[i])
    v = pbox(merge(u))
    w = v ^ k
    return w

def encrypt(p, rounds, key):
    for i in range(rounds):
        p = roundd(p, key[i])
    return p

def make_flag(k):
    param = md5(b"%x%x%x" % (k[0], k[1], k[2])).hexdigest()
    return "SharifCTF{%s}" % param

def test_subset_keys(loglines, blockno, key1, key2):
    mask = 0x3f << (bsbox*blockno)
    negmask = 0xfffffffff ^ mask
    pmask = pbox(mask)
    pnegmask = pbox(negmask)
    invmask = split(inv_p(mask))
    
    bins = [set(range(64)) for x in xrange(nsbox)]
        
    for _, pt2, ct in loglines:
        t = ct & pmask
        
        # invert xor_key2
        t = t ^ pbox(key2 << (bsbox * blockno))
        assert t & pnegmask == 0
        
        # invert perm2
        t = inv_p(t)
        assert t & negmask == 0
        
        # invert sbox2
        t = inv_s(t >> (bsbox * blockno)) << (bsbox * blockno)
        assert t & negmask == 0
        
        # invert xor_key1
        t ^= key1 << (bsbox * blockno)
        assert t & negmask == 0
        
        # invert perm1
        t = inv_p(t)
        
        t = split(t)
        for sboxno in xrange(nsbox):
            sboxmask = invmask[sboxno]
            
            # find possible inputs for sbox1
            res = set()
            for input in xrange(64):
                if input & sboxmask == t[sboxno] & sboxmask:
                    ptt = (pt2 >> (bsbox * sboxno)) & 0x3f
                    res.add(inv_s(input) ^ ptt)
                    
            bins[sboxno].intersection_update(res)
            if len(bins[sboxno]) == 0:
                return None
            
    return bins
    
def get_block_result(loglines, blockno):
    for key1 in xrange(64):
        for key2 in xrange(64):
            bins = test_subset_keys(loglines, blockno, key1, key2)
            if bins is not None:
                return key1, key2, bins

def main():
    loglines = []
    for line in open("log.txt"):
        if not line.startswith("0x"):
            continue
            
        pt, ct = line.strip().split("  ->  ")
        pt = int(pt[2:], 16)
        ct = int(ct[2:], 16)
        
        # do sbox0 and perm0
        pt2 = roundd(pt, 0)

        loglines.append((pt, pt2, ct))
        
    key0_parts = [None] * 6
    key1 = 0
    key2 = 0
    
    for blockno in xrange(nsbox):
        print "Finding keys for block", blockno
        key1_part, key2_part, bins = get_block_result(loglines, blockno)
        key1 |= key1_part << (bsbox * blockno)
        key2 |= pbox(key2_part << (bsbox * blockno))
        
        for i in xrange(nsbox):
            if len(bins[i]) == 1:
                k = list(bins[i])[0]
                assert key0_parts[i] == None or key0_parts[i] == k
                key0_parts[i] = k
        
    key0 = 0
    for blockno in xrange(nsbox):
        key0 |= key0_parts[blockno] << (bsbox * blockno)
        
    key = [key0, key1, key2]
    for pt, pt2, ct in loglines:
        assert encrypt(pt, 3, key) == ct
        
    print "Found valid key %x %x %x" % (key0, key1, key2)
    print make_flag(key)

main()
