

index = 0
def decode(data, start, size):
    global index
    for i in xrange(1, size):
        data[start + i] = (data[start + i] + data[start + i - 1]) & 0xff

    print index, repr("".join([chr(x) for x in data[start:start+size]]))
    index += 1

data = [ord(x) for x in open("library.so", "rb").read()]

decode(data, 0x3004, 20)
decode(data, 0x3018, 32)
decode(data, 0x3038, 28)
decode(data, 0x3054, 17)
decode(data, 0x3065, 12)
decode(data, 0x3071, 7)
decode(data, 0x3078, 5)
decode(data, 0x307d, 8)
decode(data, 0x3085, 12)
decode(data, 0x3091, 7)
decode(data, 0x3098, 7)
decode(data, 0x309f, 7)
decode(data, 0x30a6, 10)
decode(data, 0x30b0, 42)
decode(data, 0x30da, 24)
decode(data, 0x30f2, 24)
decode(data, 0x310a, 7)
decode(data, 0x3111, 50)
decode(data, 0x3143, 6)
decode(data, 0x3149, 5)
decode(data, 0x314e, 5)
decode(data, 0x3153, 6)
decode(data, 0x3159, 18)
decode(data, 0x316b, 4)
decode(data, 0x316f, 8)

    
open("output.so", "wb").write("".join([chr(x) for x in data]))

