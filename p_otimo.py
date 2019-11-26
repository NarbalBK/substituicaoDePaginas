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

def fifo(workList, counterList, q1, q2):
    resultList = []
    for q1 in range(q1, q2+1):
        fifoTimeStart = time.time()
        index = 0
        incidence = False
        acertos = 0
        erros = 0
        frame = [-1] * q1
        waitList = []
        cTam = len(counterList)
        for instruction in workList:
            if (index<q1):
                for i in range(q1):
                    if (instruction.pageNumber == frame[i]):
                        acertos += 1
                        incidence = True
                        for j in range(cTam):
                            if (instruction.pageNumber == counterList[j].pageNumber):
                                counterList[j].pageQtd -= 1
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
                        for j in range(cTam):
                            if (instruction.pageNumber == counterList[j].pageNumber):
                                counterList[j].pageQtd -= 1
                                break
                        
                    else:
                        soothList = sorted(counterList, key=lambda x: x.pageQtd, reverse=False)
                        for sooth in soothList:
                            aux = 0
                            for w in waitList:
                                if sooth.pageNumber == w.pageNumber:
                                    frame[w.frameIndex] = instruction.pageNumber
                                    waiter.pageNumber = instruction.pageNumber
                                    waiter.frameIndex = w.frameIndex
                                    waitList.pop(aux)
                                    waitList.append(waiter)
                                    erros += 1
                                    index += 1
                                    flag = 1
                                    break
                                aux += 1
                            if flag == 1:
                                break
                        for j in range(cTam):
                            if (instruction.pageNumber == counterList[j].pageNumber):
                                counterList[j].pageQtd -= 1
                                break
            incidence = False
            flag = 0
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


q1 = 5
q2 = 15
workFile = readFile("teste.txt")
workList = makeList(workFile)
sortWorkList = sorted(workList, key=lambda x: x.pageNumber, reverse=False)
counterList = countPages(sortWorkList)
results = (fifo(workList, counterList, q1, q2))
print(results)
makePlot(results, q1, q2)

