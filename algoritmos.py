# -*- coding: utf-8
# Stephen Marsland, 2008, 2014
# Adaptação e correção de bugs por Hendrik Macedo, 2017


import numpy as np
import time
from search import *
from utils import *

def criaTabelaRes(vetores):
    j=0
    tam = len(vetores)
    tabela = [(-1, 0, 0) for i in range(27)]

    for i in range(tam):
        tam_i = len(vetores[i])
        if i != tam-1:
            for j in range(tam_i):
                pos = ord(vetores[i][j].upper()) - 65
                valor1 = pos
                valor2 = tabela[pos][1] + 10**(tam_i - (j+1))
                #print("{} {} {}".format(vetores[i][j].upper(), pos, 10**(tam_i - (j+1))))
                if j == 0:
                    tabela[pos] = (valor1, valor2, 1)
                else:
                    tabela[pos] = (valor1, valor2, tabela[pos][2])
        else:
            for j in range(tam_i):
                pos = ord(vetores[i][j].upper()) - 65
                valor1 = pos
                valor2 = tabela[pos][1] - 10 ** (tam_i - (j + 1))
                #print("{} {} {}".format(vetores[i][j].upper(), pos, 10 ** (tam_i - (j + 1))))
                if j == 0:
                    tabela[pos] = (valor1, valor2, 1)
                else:
                    tabela[pos] = (valor1, valor2, tabela[pos][2])
    tabela_res = [x for x in tabela if x[0] != -1]
    return tabela_res

def ajustar(possibleValues,tabela):
    for i in range(len(possibleValues)):
        if possibleValues[i] == 0 and tabela[i][2] == 1:
            valor = np.random.randint(1, 9)
            if valor not in possibleValues:
                possibleValues[i] = valor
            else:
                id = get_id(possibleValues, valor)
                # print(possibleValues[id])
                temp = possibleValues[id]
                possibleValues[id] = possibleValues[i]
                possibleValues[i] = temp
    return possibleValues


def get_valor(letra,vetores,tabela):
    for i in range(len(tabela)):
        if tabela[i][0] == letra:
            return vetores[i]


def get_id(vetor,valor):
    for i in range(len(vetor)):
        if vetor[i] == valor:
            return i


def tweak(valores, tabela,n_alt):
    possibleValues = valores.copy()
    tam = len(valores)
    #pos = 0
    #alt = np.random.randint(1, len(valores))
    #alt = int(round(n_alt*len(valores)))
    #alt = 2
    for j in range(n_alt):
        pos = np.random.randint(tam)
        valor = np.random.randint(10)
        if valor not in possibleValues:
            possibleValues[pos] = valor
        else:
            id = get_id(possibleValues, valor)
            temp = possibleValues[id]
            possibleValues[id] = possibleValues[pos]
            possibleValues[pos] = temp

    possibleValues = ajustar(possibleValues, tabela)
    return possibleValues


def hillClimbing(max_alt,nTests,tabela):
    # np.shape(v) retorna um vetor que corresponde à dimensão da matriz v

    nLetras = len(tabela)

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    valores = cria_lista(nLetras)
    valores = ajustar(valores,tabela)
    soma = qualidade(valores, tabela)
    n_interacoes = 0
    alt = int(max_alt*nLetras)
    for i in range(nTests):
        if soma != 0:
            # Choose cities to swap
            possibleValues = ajustar(tweak(valores,tabela,max_alt),tabela)
            novaSoma = qualidade(possibleValues, tabela)

            if novaSoma < soma:
                soma = novaSoma
                valores = possibleValues
            n_interacoes += 1
        else:
            break

    return valores, soma, n_interacoes


def simulatedAnnealing(max_alt,nTests,tabela):
    nLetras = len(tabela)

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    valores = ajustar(cria_lista(nLetras),tabela)
    soma = qualidade(valores, tabela)
    if soma == 0:
        print("Acertou de primeira!")
    T = nTests*100
    c = 0.8
    #print(T)
    alt = int(round(max_alt * nLetras))
    # while T>1:
    n_interacoes = 0
    for i in range(nTests):
        if soma != 0:
            # Choose cities to swap
            possibleValues = ajustar(tweak(valores, tabela, alt), tabela)
            novaSoma = qualidade(possibleValues, tabela)
            if novaSoma != -1:
                if (novaSoma < soma) or (T >= 0 and np.random.rand() < np.exp((soma - novaSoma)/T)):
                    soma = novaSoma
                    valores = possibleValues

            # Annealing schedule
            T = c * T
            n_interacoes += 1
        else:
            break
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


def runHill(max_alt, nTests,termos,imprime):
    #print("\nHill Climbing")
    tabela = criaTabelaRes(termos)
    start = time.time()
    result = hillClimbing(max_alt, nTests,tabela)
    finish = time.time()
    tempo = finish - start
    if imprime:
        imprimeResultado(result[0],tabela)
        print(" Número de Interações: ", result[2])
        print(" Resultado:", result[1])
        print("Tempo:", tempo)
    if result[1] != 0:
        return 0, result[2],tempo
    else:
        return 1, result[2],tempo


def runSimAnnealing(max_alt, nTests, termos, imprime):
    #print("\nSimulated Annealing")
    tabela = criaTabelaRes(termos)
    start = time.time()
    result = simulatedAnnealing(max_alt, nTests,tabela)
    finish = time.time()
    tempo = finish - start
    if imprime:
        imprimeResultado(result[0], tabela)
        print(" Resultado:", result[1])
        print(" Número de Interações: ", result[2])
        print("Tempo:", tempo)

    if result[1] != 0:
        return 0, result[2],tempo
    else:
        return 1, result[2],tempo


def mapeamento(x):
    pos = ord(x.upper())-65
    return pos

#runHill()
#runSimAnnealing(8)

#print(mapeamento("a",[3,1,2,6,4]))
#tabela = [0 for i in range(27)]




def soma(v,t):
    termo = 0
    tam = len(v)
    for i in range(len(v)):
        valor = mapeamento(v[i])
        termo += valor * (10 ** (tam - (i + 1)))
    return termo


def qualidade(vetor, tabela):
    res = 0
    a = set(vetor)
    if len(a) < len(vetor):
        return -1
    for v in range(len(vetor)):
        res += vetor[v] * tabela[v][1]
    return abs(res)


def experimento(n_execucoes,n_iteracoes,por_tw,termos):
    res_hill = 0
    acertos_hill = 0
    acertos_sa = 0
    res_sa = 0
    tempo_hill = 0.0
    tempo_sim = 0.0
    it_certas = 0
    tem_certas = 0
    start = time.time()
    for i in range(n_execucoes):
        #hill = runHill(por_tw,n_iteracoes,termos,False)
        sim = runSimAnnealing(por_tw,n_iteracoes,termos,False)
        #res_hill += hill[1]
        res_sa += sim[1]
        if sim[0] == 1:
            it_certas += sim[1]
            tem_certas += sim[2]
        #acertos_hill += hill[0]
        acertos_sa += sim[0]
        #tempo_hill += hill[2]
        tempo_sim += sim[2]
    finish = time.time()
    #res_hill /= n_execucoes
    res_sa /= n_execucoes
    print(it_certas)
    if acertos_sa != 0:
         it_certas /= acertos_sa
         tem_certas /= acertos_sa
    else:
        it_certas = 0
    #por_hill = (float(acertos_hill) /n_execucoes)*100
    por_sa = (float(acertos_sa) / n_execucoes) * 100
    #tempo_hill/=n_execucoes
    tempo_sim/=n_execucoes
    print("Dados: ")
    print("Número de execuções: ", n_execucoes)
    print("Número de iterações: ", n_iteracoes)
    print("Tempo(em min): ", (finish-start)/60)
    print("Porcentagem de modificação do tweak:", por_tw*100, "%")
    print("Termos: ", termos)
    print("\n                                       Resultado")
    print("-----------------------------------------------------------------------------------------------------------")
    print("                     |Iterações  | Acertos(em %)| Iterações em acertos |Tempo(em s)| Tempo em acertos(em s)")
    # print("-----------------------------------------------------------------")
    # print("Hill Climbing       | {0}      |    {1:.1f}     ||    {2:.3f}".format(res_hill,por_hill,tempo_hill))
    print("------------------------------------------------------------------------------------------------------------")
    print("Simulated Annealing  | {0}      |    {1:.1f}     |       {2:.1f}          |    {3:.3f}  |   {4:.3f}         ".format(res_sa, por_sa, it_certas, tempo_sim, tem_certas))
    print("------------------------------------------------------------------------------------------------------------")
    # print("Média               | {0:.2f}       |    {1:.1f}     |    {2:.3f}".format((res_hill+res_sa)/2, (por_hill+por_sa)/2, (tempo_sim+tempo_hill)/2))
    # print("-----------------------------------------------------------------")

def cria_lista(n):
    aux = [i for i in range(10)]
    res = []
    for i in range(n):
        j = np.random.randint(0,len(aux))
        res.append(aux[j])
        aux.remove(aux[j])
    return res

experimento(2, 1000000, 0.3, ["FORTY","TEN","TEN","SIXTY"])

#runSimAnnealing(0.3,500000,["FORTY","TEN","TEN","SIXTY"],True)
#print("Lista: ", cria_lista(8))
#print(lista_aleatoria(8,criaTabelaRes(["SEND","MORE", "MONEY"])))
#print(criaTabelaRes(["POTATO", "TOMATO", "PUMPKIN"]))
#["POTATO","TOMATO", "PUMPKIN"]
#["SEND","MORE", "MONEY"]
#["FORTY","TEN","TEN","SIXTY"]