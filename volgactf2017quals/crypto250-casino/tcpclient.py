import socket, struct, os, binascii, base64, sys, hashlib
import telnetlib   

from casino_server import *

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

def solve_main(bits, source):
    nbits, poly = lfsr_solver(bits)
    state = int(bits[:nbits][::-1], 2)
    poly = poly[:nbits+1]
    # print poly
    # print state
    generator = Generator(poly, state)
    
    ncorrect = 0
    for n in source:
        t = generator.next_number(6) % 42
        if n == t:
            ncorrect += 1
            
    #print ncorrect, len(source)
    if ncorrect == len(source):
        return generator
    else:
        return None
        
    
def solve_recursive(bits, currdepth, maxdepth, source):
    if currdepth == maxdepth:
        return solve_main(bits, source)
    else:
        newbits = bin(source[currdepth])[2:].rjust(6, "0")
        res = solve_recursive(bits + newbits, currdepth + 1, maxdepth, source)
        if res:
            return res
        
        if source[currdepth] <= 21:
            newbits = bin(source[currdepth]+42)[2:].rjust(6, "0")
            res = solve_recursive(bits + newbits, currdepth + 1, maxdepth, source)
            if res:
                return res
                
        return None
        
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

def lfsr_solver(bits):
    s = [int(c) for c in bits]
        
    n = len(s)
    b = [0] * n
    c = [0] * n

    b[0] = 1
    c[0] = 1

    N = 0
    L = 0
    m = -1
    while N < n:
        d = s[N]
        for i in xrange(1, L+1):
            d ^=c [i] & s[N-i]
            
        if d == 1:
            t = list(c)
            i = 0
            while (i+N-m) < n:
                c[i+N-m] ^= b[i]
                i += 1
                
            if L <= (N >> 1):
                L = N+1-L
                m = N
                b = t
                
        N += 1
        
    return L, c
    
sc = socket.create_connection(("casino.quals.2017.volgactf.ru", 8788))
solvechall(sc)

#sc = socket.create_connection(("10.0.0.97", 12345))

for i in xrange(4):
    readline(sc)

samples = []
while True:
    sc.send("0\n")
    res = readline(sc).strip()
    if "Wrong" in res:
        n = int(res.split("The number was ")[1].split(".")[0])
    elif "Congratulations" in res:
        n = 0
    else:
        exit()
    samples.append(n)
    coins = int(res.split()[-1])
    print "my coins", coins
    readline(sc)
    if coins == 1:
        break
        
print samples
print len(samples)
bads = 0
for n in samples:
    if n <= 21:
        bads += 1
        
print 2**bads
generator = solve_recursive("", 0, 17, samples)

while True:
    next = generator.next_number(6) % 42
    sc.send(str(next) + "\n")
    for i in xrange(2):
        readline(sc)
    
while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    