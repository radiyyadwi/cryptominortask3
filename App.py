from ElGamal import *
from ElGamalKey import *

p = int(input('Masukkan nilai p : '))
g = int(input('Masukkan nilai g : '))
x = int(input('Masukkan nilai x : '))

ek = ElGamalKey(p,g,x)
ek.saveKey('a','b')
e = ElGamal('small_cat.jpg','a.pub')
e.encryption('encrypted',1520)
e.decryption('encrypted', 'b.priv')
# block = e.split_into_block()



