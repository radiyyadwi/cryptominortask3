from Tools import *

class ElGamalKey:
    # Constructor
    def __init__(self,p, g, x):
        if g >= p : 
            raise Exception("Nilai g lebih besar dari bilangan prima p")
        if x > p-2 or x < 1:
            raise Exception("Nilai x tidak sesuai")
        
        y = (g**x) % p
        self.publickey = (y,g,p)
        self.privatekey = (x,p)

    def saveKey(self, pubfilename, privfilename):
        saveArrayToFile(pubfilename + '.pub', self.publickey)
        saveArrayToFile(privfilename + '.priv', self.privatekey)