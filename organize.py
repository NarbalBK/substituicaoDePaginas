def readFile(filename):
    fileEntry = open(filename, "r")
    contents = fileEntry.read()
    return contents

class Instruction:
    pageNumber = None
    pageMode = None

class PageCounter:
    pageNumber = None
    pageQtd = 0

def makeList(workfile):
    aux = ''
    workList = []
    for i in workFile:
        if i == "-":
            pass
        else:
            instruction = Instruction()
            if i == 'R':
                instruction.pageMode = 0
                instruction.pageNumber = aux
                workList.append(instruction)
                aux = ''
            elif i == 'W':
                instruction.pageMode = 1
                instruction.pageNumber = aux
                workList.append(instruction)
                aux = ''
            else:
                aux = aux + i
    return workList

def countPages(sortWorkList):
    counterList = []
    pageCounter = PageCounter()
    pageCounter.pageNumber = sortWorkList[0].pageNumber

    for i in range(len(sortWorkList)):

        if (pageCounter.pageNumber == sortWorkList[i].pageNumber):
            pageCounter.pageQtd += 1
        else:
            counterList.append(pageCounter)
            pageCounter = PageCounter()
            pageCounter.pageNumber = sortWorkList[i].pageNumber
            pageCounter.pageQtd = 1
    counterList.append(pageCounter)

    return counterList


workFile = readFile("teste.txt")
workList = makeList(workFile)

print(workFile)
sortWorkList = sorted(workList, key=lambda x: x.pageNumber, reverse=False)
counterList = countPages(sortWorkList)

for obj in counterList:
    print(obj.pageNumber)
    print(obj.pageQtd)

