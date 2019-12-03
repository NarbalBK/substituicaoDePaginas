from random import randint

def makeFile(filename, base, size):
    fileEntry = open(filename + ".txt","w+")

    for _ in range(size):
        num = randint(1, base)
        wordSeed = randint(0, 1)
        word = 'R' if wordSeed==0 else 'W'
        fileEntry.write("%d%s-" % (num, word))

    fileEntry.close


makeFile('teste', 7, 22)