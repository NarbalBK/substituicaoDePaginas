import time
import matplotlib.pyplot as plt

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

def mur(workList, q1, q2):
    resultList = []
    for q1 in range(q1, q2+1):
        murTimeStart = time.time()
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
                        for j in range(q1):
                            if (waitList[j].frameIndex == i):
                                waiter = Waiter()
                                waiter.pageNumber = waitList[j].pageNumber
                                waiter.frameIndex = waitList[j].frameIndex
                                waitList.pop(j)
                                waitList.append(waiter)
                                break
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
                
        murTimeElapsed = time.time() - murTimeStart
        resultList.append([erros, acertos, murTimeElapsed])
    return resultList

def makePlot(results, q1, q2):
    plotAcerto = []
    plotFrame = []
    i = 0
    for q1 in range(q1, q2+1):
        plotAcerto.append(int(results[i][1]))
        plotFrame.append(q1)
        i+=1
    plt.plot(plotFrame, plotAcerto, marker='o')
    plt.xlabel('numero de frames')
    plt.ylabel('qtd de acertos')
    plt.show()


q1 = 5
q2 = 11
workFile = readFile("teste.txt")
workList = makeList(workFile)
results = (mur(workList, q1, q2))
print(results)
makePlot(results, q1, q2)

