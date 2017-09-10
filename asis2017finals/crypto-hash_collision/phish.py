nbit = 512

from Crypto.Util.number import bytes_to_long, isPrime
from hashlib import sha512

def phish(m, params):
    def pad(m):
        return m + (nbit - 6 - len(m) % (nbit - 6)) * '/'

    def auxphi(a, b, p, g, s):
        assert (len(a) - nbit)**2 + (len(b) - (nbit - 6))**2 == 0
        assert isPrime(p) and isPrime(p/2)
        assert g > 1
        q = p // 2
        if pow(g, q, p) == 1:
            h = pow(g, s, p)
            r = pow(g, int((a+b)[:nbit - 3]), p) * pow(h, int((a+b)[nbit - 3:]), p) % p
        return bin(r)[2:].zfill(nbit)

    p, g, s = params
    mbit = bin(bytes_to_long(pad(m)))[2:]
    M = [mbit[(nbit - 6)*i:(nbit - 6)*(i+1)].zfill((nbit - 6)) for i in range(len(mbit) / (nbit - 6))]
    X = ['0'*nbit]
    for i in range(len(M)):
        X.append(auxphi(X[i], M[i], p, g, s))
    return sha512(X[-1]).hexdigest()
