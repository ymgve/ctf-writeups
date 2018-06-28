import struct, sys

from PIL import Image, ImageDraw

def recurse(f, draw, xsize, ysize, xpos, ypos):
    xhalf = xsize / 2
    yhalf = ysize / 2

    xmiddle = xpos + xhalf
    ymiddle = ypos + yhalf
    
    xright = xpos + xsize
    ybottom = ypos + ysize
    
    cmd = ord(f.read(1))
    
    if cmd < 15:
        b,g,r = struct.unpack("BBB", f.read(3))
    
    if cmd & 1 == 1:
        recurse(f, draw, xhalf, yhalf, xpos, ypos)
    else:
        draw.rectangle((xpos, ypos, xmiddle, ymiddle), fill=(r,g,b))
    
    if cmd & 2 == 2:
        recurse(f, draw, xhalf, yhalf, xmiddle, ypos)
    else:
        draw.rectangle((xmiddle, ypos, xright, ymiddle), fill=(r,g,b))
        
    if cmd & 4 == 4:
        recurse(f, draw, xhalf, yhalf, xpos, ymiddle)
    else:
        draw.rectangle((xpos, ymiddle, xmiddle, ybottom), fill=(r,g,b))
    
    if cmd & 8 == 8:
        recurse(f, draw, xhalf, yhalf, xmiddle, ymiddle)
    else:
        draw.rectangle((xmiddle, ymiddle, xright, ybottom), fill=(r,g,b))

f = open(sys.argv[1], "rb")

magic, xsize, ysize = struct.unpack("<4sII", f.read(12))

sz = 1
while sz < max(xsize, ysize):
    sz *= 2
    
im = Image.new("RGB", (xsize, ysize))
draw = ImageDraw.Draw(im)

recurse(f, draw, sz, sz, 0, 0)

im.save(sys.argv[1] + ".png")