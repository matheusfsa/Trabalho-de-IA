# -*- coding: utf-8
# Stephen Marsland, 2008, 2014
# Adaptação e correção de bugs por Hendrik Macedo, 2017


import numpy as np
import time


def ajustar(solucao,tabela):
    for i in range(len(solucao)):
        if solucao[i] == 0 and tabela[i][2] == 1:
            solucao[i] = np.random.randint(1, 9)
    return solucao


def hillClimbing(tabela):
    # np.shape(v) retorna um vetor que corresponde à dimensão da matriz v

    nLetras = len(tabela)

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    valores = np.random.randint(10, size = nLetras)
    soma = qualidade(valores, tabela)
    n_interacoes = 0
    for i in range(3000):
        # Choose cities to swap
        pos = np.random.randint(nLetras)
        pos2 = np.random.randint(nLetras)
        possibleValues = valores.copy()
        possibleValues[pos] = np.random.randint(10)
        possibleValues[pos2] = np.random.randint(10)
        possibleValues = ajustar(possibleValues,tabela)
        novaSoma = qualidade(possibleValues,tabela)

        if novaSoma < soma:
            soma = novaSoma
            valores = possibleValues
        n_interacoes += 1
    return valores, soma, n_interacoes


def simulatedAnnealing(nLetras):

    valores = np.random.randint(10, size=nLetras)
    soma = quality(valores)

    T = 1000
    c = 0.8
    nTests = 5000

    # while T>1:
    n_interacoes = 0
    for i in range(nTests):
        # Choose cities to swap
        pos = np.random.randint(nLetras)
        pos2 = np.random.randint(nLetras)
        possibleValues = valores.copy()
        possibleValues[pos] = np.random.randint(10)
        possibleValues[pos2] = np.random.randint(10)
        possibleValues = ajustar(possibleValues)
        novaSoma = quality(possibleValues)

        if (novaSoma < soma) or (
            (soma - novaSoma) > T * np.log(np.random.rand())):
            soma = novaSoma
            valores = possibleValues

        # Annealing schedule
        T = c * T
        n_interacoes += 1
    return valores, soma, n_interacoes

def imprimeResultado(vetor,tabela):
    print("Resultado:")
    for i in range(len(vetor)):
        print("{} = {} ".format(chr(tabela[i][0]+65), vetor[i]))
    #print("S = ", vetor[0], " E = ", vetor[1], " N = ", vetor[2], " D = ", vetor[3], " M = ", vetor[4], " O = ",
     #     vetor[5], " R = ", vetor[6], " Y = ", vetor[7])
    #print("  {}{}{}{}".format(vetor[0], vetor[1], vetor[2], vetor[3]))
    #print("+ {}{}{}{}".format(vetor[4], vetor[5], vetor[6], vetor[1]))
    #print("----------")
    #print(" {}{}{}{}{}".format(vetor[4], vetor[5], vetor[2], vetor[1], vetor[7]))

def vetores():
    n = int(input("Quantos termos serão somados?\n"))
    print("Digite os termos da soma\n")
    res = [0 for i in range(n+1)]
    for i in range(n):
        res[i] = input("Termo " + str(i) + ": ")
    res[n] = input("Digite o termo correspondente ao resultado:")
    return res
def runHill():
    print("\nHill Climbing")
    tabela = criaTabelaRes(["SEND", "MORE", "MONEY"])
    start = time.time()
    result = hillClimbing(tabela)
    finish = time.time()
    imprimeResultado(result[0],tabela)
    print(" Número de Interações: ", result[2])
    print(" Resultado:", result[1])
    print("Tempo:", finish-start)


def runSimAnnealing(nLetras):
    print("\nSimulated Annealing")
    start = time.time()
    result = simulatedAnnealing(nLetras)
    finish = time.time()
    imprimeResultado(result[0])
    print(" Resultado:", result[1])
    print(" Número de Interações: ", result[2])
    print("Tempo:", finish - start)


def mapeamento(x):
    pos = ord(x.upper())-65
    return pos

#runHill()
#runSimAnnealing(8)

#print(mapeamento("a",[3,1,2,6,4]))
#tabela = [0 for i in range(27)]

def criaTabelaRes(vetores):
    j=0
    tam = len(vetores)
    tabela = [(0,0,0) for i in range(27)]
    for i in range(tam):
        tam_i = len(vetores[i])
        if i != tam-1:
            for j in range(tam_i):
                pos = ord(vetores[i][j].upper()) - 65;
                valor1 = pos
                valor2 = tabela[pos][1] + 10**(tam_i - (j+1))
                #print("{} {} {}".format(vetores[i][j].upper(), pos, 10**(tam_i - (j+1))))
                if j == 0:
                    tabela[pos] = (valor1, valor2,1)
                else:
                    tabela[pos] = (valor1, valor2, 0)
        else:
            for j in range(tam_i):
                pos = ord(vetores[i][j].upper()) - 65;
                valor1 = pos
                valor2 = tabela[pos][1] - 10 ** (tam_i - (j + 1))
                #print("{} {} {}".format(vetores[i][j].upper(), pos, 10 ** (tam_i - (j + 1))))
                if j == 0:
                    tabela[pos] = (valor1, valor2,1)
                else:
                    tabela[pos] = (valor1, valor2, 0)
    tabela_res = [x for x in tabela if x[0] != 0]
    return tabela_res


def soma(v,t):
    termo = 0
    tam = len(v)
    for i in range(len(v)):
        valor = mapeamento(v[i])
        termo += valor * (10 ** (tam - (i + 1)))
    return termo


def qualidade(vetor, tabela):
    res = 0
    for v in range(len(vetor)):
        res += vetor[v] * tabela[v][1]
    return abs(res)

#print(qualidade(["ABC", "BBA", "ACB"], [2, 2, 3]))
tabela = criaTabelaRes(["SEND","MORE", "MONEY"])
res = qualidade([4, 3, 1, 3, 0, 0, 9, 7],tabela)
print(res)
runHill()