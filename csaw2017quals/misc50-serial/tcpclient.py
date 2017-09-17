import socket, struct, os, binascii, base64

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

sc = socket.create_connection(("misc.chal.csaw.io", 4239))

readline(sc)

s = ""
while True:
    res = readline(sc, False)
    p = res[1:10].count("1")
    if res[0] == "1" or res[10] == "0" or p % 2 == 1:
        sc.send("0")
    else:
        s += chr(int(res[1:9], 2))
        print repr(s)
        sc.send("1")

# flag{@n_int3rface_betw33n_data_term1nal_3quipment_and_d@t@_circuit-term1nating_3quipment}