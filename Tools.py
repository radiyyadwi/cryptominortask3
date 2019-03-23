
def saveBinToFile(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

def saveToFile(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def saveArrayToFile(filename, data):
    with open(filename, "w") as f:
        for i in data:
            f.write("%s\n" % i)

def readFromFileBytes(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return data

def readFromFileString(filename):
    with open(filename, "r") as f:
        data = f.read()
    return data

def split_string_into_list_of_length_n(string, n):
    if (len(string) % n) != 0: raise Exception()
    return [string[i:i + n] for i in range(0, len(string), n)]

def split_into_block(string, max_block_size):
    block = []
    temp = ''
    i = 0
    temp_numb = 0
    while i < len(string):
        temp += string[i]
        if temp:
            temp_numb = int(temp)
        if temp == '0':
            block.append(temp)
            temp = ''
        if temp_numb >= max_block_size:
            i-=1
            block.append(temp[:-1])
            temp = ''
            temp_numb = 0
        if i == len(string)-1:
            block.append(temp)
        i+=1
    return  block