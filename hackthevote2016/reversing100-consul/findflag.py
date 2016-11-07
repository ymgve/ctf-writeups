data = open("consul.dcdcdac48cdb5ca5bc1ec29ddc53fb554d814d12094ba0e82f84e0abef065711", "rb").read()

data = data[0x1280:0x1358]

for i in xrange(256):
    s = ""
    for c in data:
        s += chr((ord(c) + i) & 0xff)
        
    if "flag" in s:
        print repr(s)