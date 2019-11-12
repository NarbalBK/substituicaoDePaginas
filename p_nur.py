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
    bitM = None

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

def nur(workList, q1, q2, deltaT):
    resultList = []
    for q1 in range(q1, q2+1):
        fifoTimeStart = time.time()
        deltaCache = deltaT
        index = 0
        incidence = False
        acertos = 0
        erros = 0
        frame = [-1] * q1
        waitList = []
        for instruction in workList:
            if (index<q1):
                waiter = Waiter()
                for i in range(q1):
                    if (instruction.pageNumber == frame[i]):
                        acertos += 1
                        incidence = True
                        for j in range(q1):
                            if (waitList[j].frameIndex == i):
                                waitList[j].bitR = 1
                                waitList[j].bitM = instruction.pageMode
                                break
                        break
                
                if (not incidence):
                    if (frame[index] == -1):
                        frame[index] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        waiter.frameIndex = index
                        waiter.bitR = 1
                        waiter.bitM = instruction.pageMode
                        waitList.append(waiter)
                        erros += 1
                        index += 1
                        
                    else:
                        min = None
                        idxMin = None
                        for i in range(q1):
                            classe = waitList[i].bitR + waitList[i].bitM*2
                            if (classe == 0):
                                idxMin = i
                                break 
                            elif (classe == 1):
                                if min != classe:
                                    min = classe
                                    idxMin = i
                            elif (classe == 2):
                                if min == None or min > 2:
                                    min = classe
                                    idxMin = i
                            elif (classe == 3):
                                if min == None:
                                    min = classe
                                    idxMin = i

                        frame[waitList[idxMin].frameIndex] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        waiter.frameIndex = waitList[idxMin].frameIndex
                        waiter.bitR = 1
                        waiter.bitM = instruction.pageMode
                        waitList.pop(idxMin)
                        waitList.append(waiter)
                        erros += 1
                        index += 1   
                            
            incidence = False
            deltaT -= 1
            if index == q1:
                index = 0
            if deltaT == 0:
                deltaT = deltaCache
                for waiter in waitList:
                    waiter.bitR = 0
                
        fifoTimeElapsed = time.time() - fifoTimeStart
        resultList.append([erros, acertos, fifoTimeElapsed])
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


q1 = 4
q2 = 11
deltaT = 5
workFile = readFile("teste.txt")
workList = makeList(workFile)
results = (nur(workList, q1, q2, deltaT))
print(results)
makePlot(results, q1, q2)