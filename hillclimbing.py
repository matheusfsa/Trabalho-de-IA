import random
import math
import numpy as np
import time

def quality(vetor):
    res = 10000*(-vetor[4]) + 1000*(vetor[0] + vetor[4] - vetor[5]) + 100*(vetor[1] +  vetor[5] - vetor[2]) + 10*(vetor[2] + vetor[6] - vetor[1]) + (vetor[3] + vetor[1] - vetor[7])
    return abs(res)
#send more money
#10000*(-vetor[4]) + 1000*(vetor[0] + vetor[4] - vetor[5]) + 100*(vetor[1] +  vetor[5] - vetor[2]) + 10*(vetor[2] + vetor[6] - vetor[1]) + (vetor[3] + vetor[1] - vetor[7])

def copy(x):
    res = [a for a in x]
    return res
def ajustar(solucao):
    for s in solucao:
        if s > 9:
            solucao[solucao.index(s)] = 9
        if s < 0:
            #print(s)
            solucao[solucao.index(s)] = 0
    if solucao[0] == 0:
        solucao[0] = np.random.randint(1, 9)
    if solucao[4] == 0:
        solucao[4] = np.random.randint(1, 9)
    return solucao
#SEND MOR Y
#[S, E, N, D, M, O, R, Y]
def hillClimbing():
    # np.shape(v) retorna um vetor que corresponde à dimensão da matriz v

    nLetras = 8

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    valores = np.random.randint(10, size = nLetras)
    soma = quality(valores)
    for i in range(1000):
        # Choose cities to swap
        pos = np.random.randint(nLetras)
        pos2 = np.random.randint(nLetras)
        possibleValues = valores.copy()
        possibleValues[pos] = np.random.randint(10)
        possibleValues[pos2] = np.random.randint(10)
        possibleValues = ajustar(possibleValues)
        novaSoma = quality(possibleValues)

        if novaSoma < soma:
            soma = novaSoma
            valores = possibleValues
    return valores, soma

def runHill():
    print ("\nHill Climbing")
    start = time.time()
    result = hillClimbing()
    finish = time.time()
    vetor = result[0]
    print("Resultado:")
    print("S = ",vetor[0], " E = ", vetor[1], " N = ", vetor[2], " D = ", vetor[3], " M = ", vetor[4], " O = ", vetor[5], " R = ", vetor[6], " Y = ", vetor[7] )
    print("  {}{}{}{}".format(vetor[0],vetor[1],vetor[2],vetor[3]))
    print("+ {}{}{}{}".format(vetor[4],vetor[5],vetor[6],vetor[1]))
    print("----------")
    print(" {}{}{}{}{}".format(vetor[4],vetor[5],vetor[2],vetor[1],vetor[7]))
    print(" Distancia:",result[1])
    print("Tempo:",finish-start)

#s = [1, 5, 0, 3, 4, 0, 3, 8]
#r = copy(s)
#print(r)
runHill()