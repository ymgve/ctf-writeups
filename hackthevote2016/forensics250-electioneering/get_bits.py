
from PIL import Image

im = Image.open("poster.d493c28eab4c4273e941326b4b6a73302016c98f1e364f1c030e0d766a865a0c.png")

bits = ""
for y in xrange(4):
    for x in xrange(44):
        if im.getpixel((x,y)) == (255,255,255):
            bits += "1"
        else:
            bits += "0"
            
res = ""
for i in xrange(0, len(bits), 8):
    res += chr(int(bits[i:i+8], 2))
    
print repr(res)
