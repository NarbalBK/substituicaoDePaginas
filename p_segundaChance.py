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

def secondChance(workList, q1, q2):
    resultList = []
    for q1 in range(q1, q2+1):
        fifoTimeStart = time.time()
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
                                break
                        break
                
                if (not incidence):
                    if (frame[index] == -1):
                        frame[index] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        waiter.frameIndex = index
                        waiter.bitR = 1
                        waitList.append(waiter)
                        erros += 1
                        index += 1
                        
                    else:
                        for _ in range(q1+1):
                            if (waitList[0].bitR == 1):
                                waitList[0].bitR = 0
                                waitList.append(waitList[0])
                                waitList.pop(0)
                            else:
                                frame[waitList[0].frameIndex] = instruction.pageNumber
                                waiter.pageNumber = instruction.pageNumber
                                waiter.frameIndex = waitList[0].frameIndex
                                waiter.bitR = 1
                                waitList.pop(0)
                                waitList.append(waiter)
                                erros += 1
                                index += 1
                                break
                                    
            incidence = False
            if index == q1:
                index = 0
                
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


q1 = 3
q2 = 11
workFile = readFile("teste.txt")
workList = makeList(workFile)
results = (secondChance(workList, q1, q2))
print(results)
makePlot(results, q1, q2)