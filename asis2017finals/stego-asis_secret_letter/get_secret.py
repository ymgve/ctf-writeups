import zlib, base64

data = open("3baa358f6d671e86f17bc4439cc4062e.jpg", "rb").read()

data = zlib.decompress(data[0x38:0x10000])

while "ASIS" not in data:
    print repr(data)
    data = base64.b64decode(data)
    
open("hidden.bin", "wb").write(data)