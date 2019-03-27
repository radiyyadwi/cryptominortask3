from Tools import *

class ElGamal:
    def __init__(self):
        pass

    def encryption(self, plainfilename, filename, pubfilename, k):
        len_bytes = []
        plainString = ''
        for i in readFromFileBytes(plainfilename):
            len_bytes.append(len(str(i)))
        for c in readFromFileBytes(plainfilename):
            plainString += str(int(c))
        encrypted = []
        publickey = readFromFileString(pubfilename).split("\n")
        block = split_into_block(plainString, int(publickey[2]))
        for i in block:
            a = (int(publickey[1]) ** k) % int(publickey[2])
            b = ((int(publickey[0]) ** k) * int(i)) % int(publickey[2])
            encrypted.append(a)
            encrypted.append(b)
        hex_encrypted=[]
        for i in encrypted:
            hex_encrypted.append(hex(i)[2:])
        print('Hasil Enkripsi : ')
        for i in hex_encrypted:
            print(i,end='')
        hex_encrypted.append(len_bytes)
        saveArrayToFile(filename,hex_encrypted)
    
    def decryption(self, encrypted_filename, decryted_filename, privatefilename):
        temp = readFromFileString(encrypted_filename).split('\n')[:-2]
        encrypted = []
        for i in temp:
            encrypted.append(int(i,16))
        len_bytes = readFromFileString(encrypted_filename).split('\n')[-2].replace('[','').replace(']','').split(',')
        encrypted = split_string_into_list_of_length_n(encrypted,2)
        result = ''
        privatekey = readFromFileString(privatefilename).split('\n')
        for i in encrypted:
            temp = (int(i[0])**(int(privatekey[1])-int(privatekey[0])-1)) % int(privatekey[1])
            result += str((int(i[1])*temp)%int(privatekey[1]))
        i=0
        j=0
        resultint = []
        while i < len(result):
            resultint.append(int(result[i:i+int(len_bytes[j])]))
            i+=int(len_bytes[j])
            j+=1
        resultbin = bytes(resultint)
        print('hasil dekripsi:')
        print(resultbin)
        saveBinToFile(decryted_filename,resultbin)