def readFile(filename):
    fileEntry = open(filename, "r")
    contents = fileEntry.read()
    return contents

print(readFile('teste.txt'))
 


