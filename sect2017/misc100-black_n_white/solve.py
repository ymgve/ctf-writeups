import binascii

data = open("chall.txt", "rb").read()

s = ""
index = 0
while index < len(data):
    if data[index] == " ":
        index += 1
        
    # U+2000	EN QUAD
    # U+2001	EM QUAD
    # U+2002	EN SPACE
    # U+2003	EM SPACE
    # U+2004	THREE-PER-EM SPACE
    # U+2005	FOUR-PER-EM SPACE
    # U+2006	SIX-PER-EM SPACE
    # U+2007	FIGURE SPACE
    # U+2008	PUNCTUATION SPACE
    # U+2009	THIN SPACE
    # U+200A	HAIR SPACE
    
    elif data[index:index+2] == "\xE2\x80":
        n = ord(data[index+2])
        if n >= 0x80 and n <= 0x8a:
            s += "%1x" % (n - 0x7e)
        else:
            s += "D"
        index += 3
    elif data[index:index+2] == "\xC2\xA0":     # NO-BREAK SPACE
        index += 2
        s += "0"
    elif data[index:index+3] == "\xE3\x80\x80": # 'IDEOGRAPHIC SPACE' (U+3000)
        index += 3
        s += "F"
    elif data[index:index+3] == "\xE1\x9A\x80": # 'OGHAM SPACE MARK' (U+1680)
        index += 3
        s += "1"
    elif data[index:index+3] == "\xE2\x81\x9F": # 'MEDIUM MATHEMATICAL SPACE' (U+205F)
        index += 3
        s += "E"
    else:
        index += 1

print repr(binascii.a2b_hex(s))