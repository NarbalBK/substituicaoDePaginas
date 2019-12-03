# coding: utf-8
import time
import matplotlib.pyplot as plt
import threading

fifoResults = []
secondChanceResults = []
nurResults = []
murResults = []
otimoResults = []

results = []

def readFile(filename):
    try:
        fileEntry = open(filename, "r")
    except IOError:
        print("Arquivo inexistente\n")
        return
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

def fifo(workList, q1, q2, fifoResults):
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
                
        fifoTimeElapsed = time.time() - fifoTimeStart
        fifoResults.append([erros, acertos, fifoTimeElapsed])
    return

def secondChance(workList, q1, q2, deltaT, secondChanceResults):
    for q1 in range(q1, q2+1):
        segTimeStart = time.time()
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
            deltaT -= 1
            if index == q1:
                index = 0
            if deltaT == 0:
                deltaT = deltaCache
                for waiter in waitList:
                    waiter.bitR = 0
                
        segTimeElapsed = time.time() - segTimeStart
        secondChanceResults.append([erros, acertos, segTimeElapsed])
    return

def nur(workList, q1, q2, deltaT, nurResults):
    for q1 in range(q1, q2+1):
        nurTimeStart = time.time()
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
                                if (waitList[j].bitM == 1):
                                    break
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
                            classe = waitList[i].bitR*2 + waitList[i].bitM
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
                
        nurTimeElapsed = time.time() - nurTimeStart
        nurResults.append([erros, acertos, nurTimeElapsed])
    return

def mur(workList, q1, q2, murResults):
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
        murResults.append([erros, acertos, murTimeElapsed])
    return

def makePlot(results, q1, q2):
    plt.figure()
    aux = q1
    for list in results:
        plotAcerto = []
        plotFrame = []
        i = 0
        q1 = aux
        for q1 in range(q1, q2+1):
            plotAcerto.append(int(list[i][1]))
            plotFrame.append(q1)
            i+=1
        plt.plot(plotFrame, plotAcerto, marker='o')
    plt.xlabel('numero de frames')
    plt.ylabel('qtd de acertos')
    plt.show()

print("Projeto II de Sistemas Operacionais")
print("Algoritmo de Substituição de Páginas\n")
print("Por: Álvaro Alves e Péricles Narbal\n")
print("Entradas do Sistema:\n")
filename = input("Entre com o nome do arquivo: ")
q1 = int(input("Defina a qunatidade INICIAL de frames: "))
q2 = int(input("Defina a quantidade FINAL de frames: "))
deltaT = int(input("Defina a zerésima do Bit R: "))

workFile = readFile(filename)
workList = makeList(workFile)

fifoThr = threading.Thread(target=fifo,args=(workList, q1, q2, fifoResults))
secondChanceThr = threading.Thread(target=secondChance,args=(workList, q1, q2, deltaT, secondChanceResults))
nurThr = threading.Thread(target=nur,args=(workList, q1, q2, deltaT, nurResults))
mruThr = threading.Thread(target=mur,args=(workList, q1, q2, murResults))

fifoThr.start()
secondChanceThr.start()
nurThr.start()
mruThr.start()

fifoThr.join()
results.append(fifoResults)
print(fifoResults)

secondChanceThr.join()
results.append(secondChanceResults)
print(secondChanceResults)

nurThr.join()
results.append(nurResults)
print(nurResults)

mruThr.join()
results.append(murResults)
print(murResults)

makePlot(results, q1, q2)