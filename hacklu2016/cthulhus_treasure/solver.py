from z3 import *
import binascii, struct

username = "cthulhu\x00\x00\x00" # gotta be cthulhu to access secret
userlen = 15 # forced minimum by code

hash = 0xdeadb00b
for i in xrange(10):
    for j in xrange(i, userlen):
        hash = 0xdeadbeef * (ord(username[i]) ^ hash)
        hash ^= (hash << 7)
        hash &= 0xffffffffffffffff
    
print "after username", hex(hash)

def findpwd(bv, hash):
    for i in xrange(0, 5):
      for j in xrange(4-i, 0, -1):
        hash = 0xcafebabe * (bv[j] ^ (4 * (bv[i] ^ hash)))
        hash = hash ^ (hash << 6)

    return hash
    
s = Solver()

bv = []
for i in xrange(4):
    t = BitVec("bv%02d" % i, 64)
    s.add(t & 0xffffffff80808080 == 0)
    s.add((t >> 0) & 0xff >= ord("a"))
    s.add((t >> 0) & 0xff <= ord("z"))
    s.add((t >> 8) & 0xff >= ord("a"))
    s.add((t >> 8) & 0xff <= ord("z"))
    s.add((t >> 16) & 0xff >= ord("a"))
    s.add((t >> 16) & 0xff <= ord("z"))
    s.add((t >> 24) & 0xff >= ord("a"))
    s.add((t >> 24) & 0xff <= ord("z"))
    bv.append(t)

t = BitVec("bv%02d" % 4, 64)
s.add(t == 0)
bv.append(t)

hash = BitVecVal(hash, 64)
s.add(findpwd(bv, hash) == 0xeeedc4e74f7b2012)

print s.check()
m = s.model()

res = ""
for i in xrange(5):
    res += struct.pack("<I", int(str(m[bv[i]])))
print repr(res)


# Who demands access to the treasure? cthulhu
# If you are who you claim to be tell me cthulhu's passphrase! &_~]3yh,0A1ACft*
# ... was only teasing you, of course I recognized you the moment you showed up at the door
# Here is your treasure: flag={c0llatzC0nj3cture}

# ilvdctwyhcsxwegn