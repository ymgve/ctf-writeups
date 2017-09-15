import socket, struct, os, binascii, base64, random, time
import telnetlib   

def readline(sc, show = True):
    res = ""
    while len(res) == 0 or res[-1] != "\n":
        data = sc.recv(1)
        if len(data) == 0:
            print(repr(res))
            raise Exception("Server disconnected")
        res += data.decode('utf-8')
        
    if show:
        print(repr(res[:-1]))
    return res[:-1]

def read_until(sc, s):
    res = ""
    while not res.endswith(s):
        data = sc.recv(1)
        if len(data) == 0:
            print(repr(res))
            raise Exception("Server disconnected")
        res += data.decode('utf-8')
        
    return res[:-(len(s))]
    
nums = {}
for line in open("halfsteps_opt.txt", "r"):
    m, e1 = (int(x) for x in line.split())
    nums[m] = e1
    
print("Precompute table length", len(nums))

g = 201527
gi = 46850207637898614761490855415476805920992830084250638354979938895293405852625477114040582143359511132171208782522093343201878578891788601077754932103520895522613928398899540158524358372481040438828294389314953430165485840948615065429401707555750296744261017884859807898233819857482588099061233309186607671119
p = 156920319682269547550840440422064789702830774969897260932124088315247211163110865017305817005797304213752612556763228047723789794713560055335007282974774888844332820576469678725018919853260647462367864702092052584778617621806467695299678199684012931325300660671488872927592192102428093535426026544017575524159

found = False
while True:
    sc = socket.create_connection(("crypto.sect.ctf.rocks", 31337))

    read_until(sc, "Submit...\n")
    sc.send(b"2\n")
    readline(sc)
    g = int(readline(sc).split(" = ")[1])
    p = int(readline(sc).split(" = ")[1])
    a = int(readline(sc).split(" = ")[1])

    print("searching")

    start = time.time()
    while time.time() < (start + 175):
        e2 = 1 << 127
        for j in range(5):
            e2 |= (1 << random.randint(1, 126))
            
        m = (a * pow(gi, e2, p)) % p
        m = m & 0xffffffffffffffff
        if m in nums:
            e1 = nums[m]
            e = e1 + e2
            print(bin(e1))
            print(bin(e2))
            print(bin(e))
            print(e)
            if pow(g, e, p) == a:
                found = True
                break
            
    if found:
        sc.send((str(e) + "\n").encode("utf-8"))
        break
        
    sc.close()

while True:
    data = sc.recv(16384)
    if len(data) == 0:
        break
    for line in data.split(b"\n"):
        print(repr(line))
    
