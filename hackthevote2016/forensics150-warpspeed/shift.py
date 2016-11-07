from PIL import Image

im = Image.open("warp_speed.5978d1405660e365872cf72dddc7515603f657f12526bd61e56feacf332cccad.jpg")

im2 = Image.new("RGB", (504, 500))

for y in xrange(500):
    for x in xrange(504):
        xx = x + (y / 8) * 504
        yy = y % 8
        
        try:
            p = im.getpixel((xx % 1000, yy + (xx / 1000) * 8))
            im2.putpixel((x,y), p)
        except IndexError:
            pass
        
im2.save("res.png")
