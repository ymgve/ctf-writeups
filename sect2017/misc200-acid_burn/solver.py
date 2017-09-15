from PIL import Image

im = Image.open("chall.webp")

w, h = im.size

for y in xrange(h):
    for x in range(w):
        p = im.getpixel((x, y))
        if p == (4, 3, 0):
            p = (255, 255, 255)
        else:
            p = (0, 0, 0)
            
        im.putpixel((x, y), p)
            
im.save("solution.png")

# SECT{I_LOVE_CRASH_OVERFLOW_BUT_I_CAN_NOT_TELL_HIM_HOW_I_FEEL_ABOUT_HIM}