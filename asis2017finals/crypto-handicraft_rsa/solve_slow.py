import base64

from Crypto.Util.number import *
from Crypto.PublicKey import RSA

def gcd(a,b):
	while b != 0:
		t = b
		b = a % b
		a = t
	return a

# Pollard's p-1 algorithm
# https://en.wikipedia.org/wiki/Pollard%27s_p_%E2%88%92_1_algorithm
# this is really slow on stock python2, use either python3 or some JITer

def factor(n):
    a = 2
    b = 2
    while True:
        if b % 10000 == 0:
            print(b)
            
        a = pow(a, b, n)
            
        p = gcd(a - 1, n)
        if 1 < p < n:
            print("FOUND " + str(p))
            return p
            
        b += 1

def decrypt(n, p, q):
    assert p * q == n

    e = 65537
    d = inverse(e, (p-1)*(q-1))

    key = RSA.construct((long(n), long(e), long(d), long(p), long(q)))
    msg = base64.b64decode("eER0JNIcZYx/t+7lnRvv8s8zyMw8dYspZlne0MQUatQNcnDL/wnHtkAoNdCalQkpcbnZeAz4qeMX5GBmsO+BXyAKDueMA4uy3fw2k/dqFSsZFiB7I9M0oEkqUja52IMpkGDJ2eXGj9WHe4mqkniIayS42o4p9b0Qlz754qqRgkuaKzPWkZPKynULAtFXF39zm6dPI/jUA2BEo5WBoPzsCzwRmdr6QmJXTsau5BAQC5qdIkmCNq7+NLY1fjOmSEF/W+mdQvcwYPbe2zezroCiLiPNZnoABfmPbWAcASVU6M0YxvnXsh2YjkyLFf4cJSgroM3Aw4fVz3PPSsAQyCFKBA==")
    
    for _ in xrange(20):
        enc = key.decrypt(msg)
        msg = enc
        
    print repr(msg)


asciikey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq+m7iHurBa9G8ujEiTpZ
71aHOVNhQXpd6jCQNhwMN3hD6JHkv0HSxmJwfGe0EnXDtjRraWmS6OYzT4+LSrXs
z9IkWGzRlJ4lC7WHS8D3NWIWYHCP4TRt2N0TlWXWm9nFCrEXqQ3IWgYQpQvKzsds
etnIZJL1tf1wQzGE6rbkbvURlUBbzBSuidkmi0kY5Qxp2Jfb6OUI647zx2dPxJpD
ffSCNffVIDUYOvrgYxIhs5HmCF3XECC3VfaKtRceL5JM8R0qz5nVU2Ns8hPvSVP+
7/i7G447cjW151si0joB7RpBplu44Vk8TXXDAk0JZdW6KwJn7ITaX04AAAAAAAAA
AQIDAQAB
-----END PUBLIC KEY-----"""

key = RSA.importKey(asciikey)
n = int(key.n)

# p = 139457081371053313087662621808811891689477698775602541222732432884929677435971504758581219546068100871560676389156360422970589688848020499752936702307974617390996217688749392344211044595211963580524376876607487048719085184308509979502505202804812382023512342185380439620200563119485952705668730322944000000001
p = factor(key.n)

q = n / p

decrypt(n, p, q)
