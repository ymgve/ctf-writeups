s = [59, 21, 25, 32, 30, 3, 63, 38, 5, 29, 40, 53, 17, 56, 58, 37, 45, 43, 52, 61, 7, 55, 57, 12, 26, 13, 49, 16, 36, 8, 31, 41, 20, 51, 33, 15, 1, 0, 23, 27, 35, 18, 47, 62, 14, 60, 10, 54, 46, 50, 9, 48, 24, 28, 44, 2, 6, 34, 19, 42, 11, 39, 22, 4]

for outputbit in xrange(6):
    zeros = set()
    ones = set()
    for i in xrange(64):
        res = (s[i] >> outputbit) & 1
        if res == 0:
            zeros.add(i)
        else:
            ones.add(i)
            
    for mask in xrange(64):
        zeros_masked = set(a & mask for a in zeros)
        ones_masked = set(a & mask for a in ones)
            
        res = zeros_masked.intersection(ones_masked)
                
        if len(res) == 0:
            print outputbit, bin(mask)
