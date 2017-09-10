import hashlib

for i in xrange(65536):
    s = "%04x" % i
    if hashlib.sha1(s).hexdigest().startswith(s):
        print s

# hashcat64 -m 100 -a 3 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9 ?a?a?a?a?a?a
#    9:-*)b 
# 57d9:-*)b53a
