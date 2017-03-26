import socket, struct, os, binascii, base64, sys, hashlib
import telnetlib   

try:
    import psyco; psyco.full()
except ImportError:
    pass


def readline(sc, show = True):
    res = ""
    while len(res) == 0 or res[-1] != "\n":
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            raise Exception("Server disconnected")
        res += data
        
    if show:
        print repr(res[:-1])
    return res[:-1]

def read_until(sc, s):
    res = ""
    while not res.endswith(s):
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            raise Exception("Server disconnected")
        res += data
        
    return res[:-(len(s))]
    
def read_all(sc, n):
    data = ""
    while len(data) < n:
        block = sc.recv(n - len(data))
        if len(block) == 0:
            print repr(data)
            raise Exception("Server disconnected")
        data += block

    return data

def I(n):
    return struct.pack("<I", n)
    
def Q(n):
    return struct.pack("<Q", n)

def find_sol(src):
    for a in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
     for b in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
      for c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
       for d in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for e in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            cand = src+a+b+c+d+e
            t = hashlib.sha1(cand).hexdigest()
            if t.endswith("ffffff") and t[-7] in ("37bf"):
                print "found", cand, t
                return cand
                
    print "NO SOL FOUND"
    exit()
    
def solvechall(sc):
    # Solve a puzzle: find an x such that 26 last bits of SHA1(x) are set, len(x)==29 and x[:24]=='e7f0de3f783bd45adcef43ed'
    res = readline(sc)
    src = res.split("x[:24]=='")[1].split("'")[0]
    print src
    sc.send(find_sol(src) + "\n")

def use_oracle(sc, ciphertext):
    global ts
    s = ""
    while len(s) < 16:
        for c in xrange(256):
            print c,
            block2 = ciphertext
            block1 = "\x00" * (15 - len(s))
            for byte in chr(c) + s:
                block1 += chr(ord(byte) ^ (len(s) + 1))
                
            sc.send(base64.b64encode("\x00" + struct.pack(">q", ts) + block1 + block2 + "\x00" * 10) + "\n")
            ts += 2
            
            res = readline(sc, False)
            res = base64.b64decode(res)
            if res[0] != "\xa2":
                s = chr(c) + s
                print repr(s)
                break
                
    return s

def xor(s, key):
    res = ""
    for i in xrange(len(s)):
        res += chr(ord(s[i]) ^ ord(key[i % len(key)]))
        
    return res
    
ct = '\xab\xb9\xe8\x22\x05\xad\xef\xa2\xfa\xdf\x37\xe5\x90\xfe\x2f\x2b\x5b\x9f\xef\x4d\xb9\x11\x88\xfb\x58\x18\xf5\xa6\x63\xa7\x10\xf3'

sc = socket.create_connection(("oracle.quals.2017.volgactf.ru", 8789))
solvechall(sc)

ts = 0

block0 = use_oracle(sc, ct[0:16])
print repr(block0)
block1 = use_oracle(sc, ct[16:32])
print repr(block1)
    
flag = block0 + xor(ct[0:16], block1)
print repr(flag)

# block0 VolgaCTF{B3w4r3_
# block1 '\x9b\xdf\xb7r1\xc9\x8b\x93\x94\xb8J\xe0\x95\xfb*.'

# result VolgaCTF{B3w4r3_0f_P4dd1ng}
