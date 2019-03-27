from ElGamal import *
from ElGamalKey import *
from ECC import *

print('=====ElGamal + ECCEG=====')
print('1. Enkripsi ElGamal')
print('2. Dekripsi ElGamal')
print('3. Enkripsi ECCEG')
print('4. Dekripsi ECCEG')

opt = int(input('Masukkan pilihan enkripsi/dekripsi : '))
if opt == 1:
    p = int(input('Masukkan nilai p : '))
    g = int(input('Masukkan nilai g : '))
    x = int(input('Masukkan nilai x : '))
    k = int(input('Masukkan nilai k : '))
    ek = ElGamalKey(p,g,x)
    stringfile = str(input('Masukkan nama File yang di enkrip : '))
    cipherfile = str(input('Masukkan nama File hasil enkrip : '))
    publicfilename = str(input('Masukkan nama file public key (tanpa extension) : '))
    privatefilename = str(input('Masukkan nama file private key (tanpa extension) : '))
    ek.saveKey(publicfilename,privatefilename)
    e = ElGamal()
    e.encryption(stringfile,cipherfile,publicfilename + '.pub',k)

if opt == 2:
    e = ElGamal()
    privatefilename = str(input('Masukkan nama file private key (tanpa extension) : '))
    encryptedfilename = str(input('Masukkan nama file yang akan di decrypt : '))
    decryptedfilename = str(input('Masukkan nama file hasil decrypt : '))
    e.decryption(encryptedfilename, decryptedfilename, privatefilename + '.priv')

if opt == 3:
    print('menu 3')

if opt == 4:
    print('menu 4')