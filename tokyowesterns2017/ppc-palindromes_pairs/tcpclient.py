import socket, struct, os, binascii, base64
import telnetlib   

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

    
sc = socket.create_connection(("ppc1.chal.ctf.westerns.tokyo", 8765))

read_until(sc, "----- START -----\n")

for caseno in xrange(50):
    readline(sc)
    readline(sc)
    fragments = readline(sc).split()
    pals = 0
    for i in xrange(len(fragments)):
        for j in xrange(len(fragments)):
            s = fragments[i] + fragments[j]
            if s == s[::-1]:
                pals += 1
    print "think it's", pals
    sc.send(str(pals) + "\n")
    readline(sc)
    readline(sc)
    
while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    