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
    litIndex = None
    bitR = None

# class IndexPath:
#     pageNumber = None
#     index = None

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

def otimo(workList, q1, q2):
    resultList = []
    for q1 in range(q1, q2+1):
        otimoTimeStart = time.time()
        index = 0
        incidence = False
        acertos = 0
        erros = 0
        frame = [-1] * q1
        waitList = []
        tamWorkList = len(workList)
        for inst in range(tamWorkList):
            instruction = workList[0]
            workList.pop(0)
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
                        indexList = []
                        max = len(workList)
                        for w in waitList:
                            for k in range(max):
                                if (w.pageNumber == workList[k].pageNumber):
                                    w.litIndex = k
                                    indexList.append(w)
                                    break
                            if w.litIndex == None:
                                w.litIndex = 1 * 10**6
                                indexList.append(w)
                        
                        sortIndex = sorted(indexList, key=lambda x: x.litIndex, reverse=True)

                        frame[sortIndex[0].frameIndex] = instruction.pageNumber
                        waiter.pageNumber = instruction.pageNumber
                        for i in range(q1):
                            if (sortIndex[0].pageNumber == waitList[i].pageNumber):
                                waiter.frameIndex = waitList[i].frameIndex
                                waitList.pop(i)
                                break
                        waitList.append(waiter)
                        erros += 1
                        index += 1

            incidence = False
            if index == q1:
                index = 0
                
        otimoTimeElapsed = time.time() - otimoTimeStart
        resultList.append([erros, acertos, otimoTimeElapsed])
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


q1 = 70
q2 = 70
workFile = readFile("teste.txt")
workList = makeList(workFile)
results = (otimo(workList, q1, q2))
print(results)
makePlot(results, q1, q2)

