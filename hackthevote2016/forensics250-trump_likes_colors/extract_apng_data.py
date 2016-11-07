import struct, binascii, zlib, hashlib

from PIL import Image

try:
    import psyco; psyco.full()
except ImportError:
    pass

def main():
    f = open("trump_likes_colors.bcddf8152cf2848c058310655c280a7dbb4f22fcc3687f00a26b6e9a57657dc4.png", "rb")

    of = open("rawresult.raw", "wb")
    
    f.read(8)
    color = 0xff0000
    
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
        if len(data) != chunksize:
            raise Exception
            
        crc = f.read(4)
        if len(crc) != 4:
            raise Exception
        
        if zlib.crc32(chunktype + data) & 0xffffffff != struct.unpack(">L", crc)[0]:
            print "%08x %08x" % (zlib.crc32(chunktype + data) & 0xffffffff, struct.unpack(">L", crc)[0])
            raise Exception
            
        elif chunktype == "fcTL":
            seqnum, width, height, xoffset, yoffset, delay_num, delay_den, dispose_op, blend_op = struct.unpack(">IIIIIHHBB", data)
            print seqnum, width, height, xoffset, yoffset, delay_num, delay_den, dispose_op, blend_op

        elif chunktype == "IDAT":
            print "%06x" % color
            of.write(binascii.a2b_hex("%06x" % color))
            
        elif chunktype == "fdAT":
            prevcolor = color
            
            h = hashlib.md5(data[4:]).hexdigest()
            if h == "f87d68ebe7be4bce27b76dee95b0f7c8" and xoffset == 2:
                color &= 0x00ffff
            elif h == "a5e3c80e897172c8449c17c37dd99d89" and xoffset == 10:
                color |= 0x0000ff
            elif h == "6517a263e85178270d9272760731f32a" and xoffset == 0:
                pass
            elif h == "31a5b0b86e28237fb5920dcf4d74a163" and xoffset == 6:
                color |= 0x00ffff
            elif h == "62ce036ad233657fba55a1889e9cc9ad" and xoffset == 6:
                color |= 0x00ff00
            elif h == "0ef375852641faa5a022774b704b086d" and xoffset == 2:
                color |= 0xffff00
            elif h == "3b3402545dc1da0a1c670bc32931c320" and xoffset == 2:
                color |= 0xff0000
            elif h == "87aab7771f89365bea47cdbbac3bf701" and xoffset == 2:
                color = 0xff00ff
            elif h == "298e1d4e7870e8950244ac5ce21ce2bf" and xoffset == 2:
                color = 0xffffff
            elif h == "36541036eae5eb719f9c77a3cc147f96" and xoffset == 2:
                color = 0x000000
            else:
                print h, xoffset
                exit()
                
                
            print "%06x" % color
            of.write(binascii.a2b_hex("%06x" % color))
            
            if dispose_op == 0:
                pass
            elif dispose_op == 2:
                color = prevcolor
            else:
                raise Exception

    
main()
