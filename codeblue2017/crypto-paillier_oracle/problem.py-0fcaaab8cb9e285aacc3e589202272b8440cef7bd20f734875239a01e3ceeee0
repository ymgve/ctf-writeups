from Crypto.Util.number import *
from Crypto.Random.random import randint
from Crypto.Random import atfork
from Crypto.Hash import SHA256

import SocketServer
import threading
import random
import string
import signal
import gmpy
import time
import key
import os

PORT = 7485
FLAG = long(key.FLAG.encode("hex"), 16)

def L(u, n):
  return (u - 1) // n

def get_random_prime(bits=1024):
  return int(gmpy.next_prime(randint(2**(bits-1), 2**bits)))

def gen_key(bits=1024):
  while True:
    p = get_random_prime(bits)
    q = get_random_prime(bits)
    if p != q and gmpy.gcd(p*q, (p-1)*(q-1)) == 1:
      break
  n = p*q
  l = int(gmpy.lcm(p-1, q-1))
  while True:
    g = randint(1, n**2)
    if gmpy.gcd(g, n**2) == 1:
      break
  u = gmpy.invert(L(pow(g, l, n**2), n), n)
  return (n, g), (l, u)

def encrypt(pk, m):
  assert m < pk[0]
  while True:
    r = randint(1, pk[0])
    if gmpy.gcd(r, pk[0]) == 1:
      break
  c1 = pow(pk[1], m, pk[0]**2)
  c2 = pow(r, pk[0], pk[0]**2)
  return (c1*c2) % pk[0]**2

def decrypt(pk, sk, c):
  m1 = L(pow(c, sk[0], pk[0]**2), pk[0])
  return (m1 * sk[1]) % pk[0]

def proof_of_work(req):
  random.seed(int(os.urandom(8).encode('hex'), 16))
  proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
  digest = SHA256.new(proof).hexdigest()
  req.sendall("SHA256(XXXX+%s) == %s\n" % (proof[4:],digest))
  req.sendall('What is XXXX? ')
  x = req.recv(1024).strip()
  if len(x) != 4 or SHA256.new(x+proof[4:]).hexdigest() != digest: 
    exit(0)
  return

class incoming(SocketServer.BaseRequestHandler):
  def handle(s):
    atfork()
    signal.alarm(1200)
    req = s.request

    def write(m):
      req.sendall(m)

    def writeline(m):
      write(m + "\n")

    def readline():
      buf = ""
      while True:
        buf += req.recv(1)
        if buf.endswith("\n"):
          break
      return buf

    proof_of_work(req)
    writeline("Welcome to the Flag Decryption Challenge!")
    write("Generating the key...")
    pk, sk = gen_key()
    writeline("Done.")
    writeline("Public key is here: (%d, %d)" % pk)
    writeline("...and Encrypted Flag: %d" % encrypt(pk, FLAG))
    while True:
      writeline("Your ciphertext here: ")
      c = long(readline())
      m = decrypt(pk, sk, c)
      writeline("LSB is %d" % (m & 1))

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
  pass

if __name__ == "__main__":
  SocketServer.TCPServer.allow_reuse_address = True
  server = ReusableTCPServer(("0.0.0.0", PORT), incoming)
  print "Listening on port %d" % PORT
  server.serve_forever()
