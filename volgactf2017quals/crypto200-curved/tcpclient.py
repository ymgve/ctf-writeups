import socket, struct, os, binascii, base64
import telnetlib

from curved_server import *

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

def ecdsa_solver(cmd):
    dA = import_private_key('.') # private key is dummy value here
    QA = import_public_key('.')
    QA = Point(NIST384, QA[0], QA[1])

    signature = ECDSA(G, dA)

    cmd1 = 'exit'
    cmd2 = 'leave'
    (r1, s1) = import_cmd_signature(cmd1, '.')
    (r2, s2) = import_cmd_signature(cmd2, '.')
    assert r1 == r2
    
    e = int(hashlib.sha512(cmd1).hexdigest(), 16)
    z1 = e >> (512 - signature.Ln)

    e = int(hashlib.sha512(cmd2).hexdigest(), 16)
    z2 = e >> (512 - signature.Ln)
        
    z = (z1 - z2)
    s = (s1 - s2)
    r_inv = invert(r1, QA.curve.n)
    s_inv = invert(s, QA.curve.n)
    k = (z * s_inv) % QA.curve.n
    dA = int((r_inv * (s1 * k - z1)) % QA.curve.n)

    signature = ECDSA(G, dA)
    r, s = signature.sign(cmd)
    assert (signature.verify(cmd, r, s, QA))
    return r, s
    
cmd = "cat flag"
r, s = ecdsa_solver(cmd)
print r, s

sc = socket.create_connection(("curved.quals.2017.volgactf.ru", 8786))
solvechall(sc)

sc.send("%d %d %s\n" % (r, s, cmd))

# t = telnetlib.Telnet()                                                  
# t.sock = sc
# t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    