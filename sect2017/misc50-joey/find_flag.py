import struct, zlib

flag = [""] * 100

def main():
    f = open("chall.png", "rb")

    f.read(8)
    idats = []
    others = {}
    while True:
        t = f.read(4)
        if len(t) == 0:
            break
        elif len(t) != 4:
            raise Exception
            
        chunksize = struct.unpack(">L", t)[0]
        
        chunktype = f.read(4)
        if len(chunktype) != 4:
            raise Exception
            
        data = f.read(chunksize)
        crc = f.read(4)
            
        if chunktype == "iTXt":
            res = zlib.decompress(data[29:])
            pos = int(res[1:])
            flag[pos] = res[0]

        else:
            others[chunktype] = data
            
    print "".join(flag)
    
main()
