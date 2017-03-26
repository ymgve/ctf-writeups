import struct

def rotl(n, bits):
    dist = bits % 32
    n = n & 0xffffffff
    return ((n << dist) | (n >> (32-dist))) & 0xffffffff

def rotr(n, bits):
    dist = bits % 32
    n = n & 0xffffffff
    return ((n << (32-dist)) | (n >> dist)) & 0xffffffff
    
class RC5(object):
    def __init__(self, key):
        nrounds = 16
        t = nrounds * 2 + 2
        S = [0xb7e15163]
        for i in xrange(1, t):
            S.append((S[-1] + 0x9e3779b9) & 0xffffffff)
            
        A = 0
        B = 0
        i = 0
        j = 0
        
        L = list(key)
        
        for ii in xrange(3 * max(t, len(key))):
            A = S[i] = rotl(S[i] + A + B, 3)
            B = L[j] = rotl(L[j] + A + B, A + B)
            i = (i + 1) % t
            j = (j + 1) % len(key)
            
        self.nrounds = nrounds
        self.t = t
        self.S = S
        
    def encrypt_block(self, A, B):
        A = (A + self.S[0]) & 0xffffffff
        B = (B + self.S[1]) & 0xffffffff
        for i in xrange(1, self.nrounds+1):
            A = (rotl(A ^ B, B) + self.S[2*i]) & 0xffffffff
            B = (rotl(B ^ A, A) + self.S[2*i+1]) & 0xffffffff
            
        return A, B
        
    def decrypt_block(self, A, B):
        for i in xrange(self.nrounds, 0, -1):
            B = rotr(B - self.S[2*i+1], A) ^ A
            A = rotr(A - self.S[2*i], B) ^ B
            
        B = (B - self.S[1]) & 0xffffffff
        A = (A - self.S[0]) & 0xffffffff
    
        return A, B
        
r0 = RC5((0xa89193a0, 0x5c3987ca))
r1 = RC5((0x32af5f86, 0x74719560))

f = open("ciphertext.zip.enc", "rb")
nonce = struct.unpack("<I", f.read(4))[0]
data = f.read()

of = open("ciphertext.zip", "wb")
for i in xrange(0, len(data) / 8):
    kA, kB = r0.encrypt_block(nonce, i)
    A, B = struct.unpack("<II", data[i*8:i*8+8])
    if i % 4 != 3:
        A ^= kA
        B ^= kB
        A, B = r1.decrypt_block(A, B)
    of.write(struct.pack("<II", A, B))
of.close()

