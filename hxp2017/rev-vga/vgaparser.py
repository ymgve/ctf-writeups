from PIL import Image

im = Image.open("vga.png")

# PNG palette indexes does not correspond to VGA palette indexes, so we have to translate
trans = [5, 3, 9, 14, 7, 6, 2, 11, 0, 15, 1, 12, 4, 10, 8, 13]

xs, ys = im.size

xsplits = set()
xsplits.add(0)
for y in xrange(ys):
    for x in xrange(xs-1):
        if im.getpixel((x, y)) != im.getpixel((x+1, y)):
            xsplits.add(x+1)
            
ysplits = set()
ysplits.add(0)
for x in xrange(xs):
    for y in xrange(ys-1):
        if im.getpixel((x, y)) != im.getpixel((x, y+1)):
            ysplits.add(y+1)
            
xsplits = sorted(xsplits)
ysplits = sorted(ysplits)

s = ""
for y in xrange(0, len(ysplits), 2):
    for x in xrange(len(xsplits)):
        fg = im.getpixel((xsplits[x], ysplits[y]))
        bg = im.getpixel((xsplits[x], ysplits[y+1]))
        t = (trans[bg] << 4) | trans[fg]
        s += chr(223)
        s += chr(t)
        
print repr(s)

print len(xsplits)
print len(ysplits)

open("vgaloader.bin", "wb").write(s)
