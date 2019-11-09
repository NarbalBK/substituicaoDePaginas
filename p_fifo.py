def readFile(filename):
    fileEntry = open(filename, "r")
    contents = fileEntry.read()
    return contents

class Instruction:
    pageNumber = None
    pageMode = None

class Waiter:
    pageNumber = None
    frameIndex = None
    bitR = None

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

def fifo(workList, q1, q2):
    resultList = []
    for q1 in range(q1, q2+1):
        index = 0
        incidence = False
        acertos = 0
        erros = 0
        frame = [-1] * q1
        waitList = []
        for instruction in workList:
            if (index<q1):
                for i in range(q1):
                    if (instruction.pageNumber == frame[i]):
                        acertos += 1
                        incidence = True
                        break
                
                if (not incidence):
                    waiter = Waiter()
                    if (frame[index] == -1):
                        frame[index] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        waiter.frameIndex = index
                        waitList.append(waiter)
                        erros += 1
                        index += 1
                        
                    else:
                        frame[waitList[0].frameIndex] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        waiter.frameIndex = waitList[0].frameIndex
                        waitList.pop(0)
                        waitList.append(waiter)
                        erros += 1
                        index += 1

            incidence = False
            if index == q1:
                index = 0

        resultList.append([erros, acertos])
    return resultList

                    

workFile = readFile("teste.txt")
workList = makeList(workFile)

print(fifo(workList, 5, 11))

