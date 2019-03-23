from Tools import *

class ElGamal:
    def __init__(self, plainfilename, pubfilename):
        string = ''
        len_bytes = []
        for i in readFromFileBytes(plainfilename):
            len_bytes.append(len(str(i)))
        for c in readFromFileBytes(plainfilename):
            string += str(int(c))

        self.publickey = readFromFileString(pubfilename).split("\n")
        self.plainString = string
        self.len_bytes = len_bytes

    def __split_into_block(self):
        block = split_into_block(self.plainString, int(self.publickey[2]))
        return  block

    def encryption(self, filename, k):
        encrypted = []
        block = self.__split_into_block()
        for i in block:
            a = (int(self.publickey[1]) ** k) % int(self.publickey[2])
            b = ((int(self.publickey[0]) ** k) * int(i)) % int(self.publickey[2])
            encrypted.append(a)
            encrypted.append(b)
        saveArrayToFile(filename,encrypted)
    
    def decryption(self, encrypted_filename, privatefilename):
        encrypted = readFromFileString(encrypted_filename).split('\n')
        encrypted = split_string_into_list_of_length_n(encrypted[:-1],2)
        result = ''
        privatekey = readFromFileString(privatefilename).split('\n')
        for i in encrypted:
            temp = (int(i[0])**(int(self.publickey[2])-int(privatekey[0])-1)) % int(privatekey[1])
            result += str((int(i[1])*temp)%int(privatekey[1]))
        i=0
        j=0
        resultint = []
        while i < len(result):
            resultint.append(int(result[i:i+self.len_bytes[j]]))
            i+=self.len_bytes[j]
            j+=1
        resultbin = bytes(resultint)
        saveBinToFile('decrypted',resultbin)

        




            
        
    
