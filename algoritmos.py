# -*- coding: utf-8
# Stephen Marsland, 2008, 2014
# Adaptação e correção de bugs por Hendrik Macedo, 2017


import numpy as np
import time
# função que recebe os termos da soma e retorna uma tabela para auxiliar o algoritmo
def criaTabelaRes(vetores):
    j=0
    tam = len(vetores)
    # A tabela possui três colunas.
    # 1ª coluna: posições da letra no vetor solução, se o valor=-1 a letra não pertence a soma.
    # 2ª coluna: soma do valores posicionais da letra
    # 3ª coluna: indica se a letra é primeira de algum termo
    tabela = [(-1, 0, 0) for i in range(27)]
    
    for i in range(tam):
        tam_i = len(vetores[i])
        if i != tam-1:
            # Os primeiros termos da soma
            for j in range(tam_i):
                # valor da letra
                valor1= ord(vetores[i][j].upper()) - 65
                valor1 = pos
                valor2 = tabela[pos][1] + 10**(tam_i - (j+1))
                if j == 0:
                    tabela[pos] = (valor1, valor2, 1)
                else:
                    tabela[pos] = (valor1, valor2, tabela[pos][2])
        else:
            for j in range(tam_i):
                pos = ord(vetores[i][j].upper()) - 65
                valor1 = pos
                valor2 = tabela[pos][1] - 10 ** (tam_i - (j + 1))
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

# max_alt: a porcentagem de posições que serão alteradas no tweak
# nTests: número máximo de iterações
# tabela: a tabela que contém a soma dos valores posicionais de cada letra
def simulatedAnnealing(max_alt,nTests,tabela):
    nLetras = len(tabela)

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    # A função ajustar, modifica o vetor para que o vetor respeite as restrições
    # valores é um vetor gerado aleatóriamentes, mas que respeita as restrições
    valores = ajustar(cria_lista(nLetras),tabela)
    # qualidade é uma função que retorna o valor da solução
    
    soma = qualidade(valores, tabela)
    T = nTests*100
    c = 0.8
    #print(T)
    # alt é o numero de posições da solução que serão alteradas
    alt = int(round(max_alt * nLetras))
    n_interacoes = 0
    for i in range(nTests):
        # Caso de parada: Encontrou  a solução ótima, ou seja soma = 0, ou passou o tempo de execução
        #o algoritmo não para quando T=0, ele passa a ter o comportamento do hill climbing
        # soma é o valor da solução atual
        if soma != 0:
            # Choose cities to swap
            # possibleValues é uma solução gerada  a partir do tweak na solução atual
            possibleValues = ajustar(tweak(valores, tabela, alt), tabela)
            novaSoma = qualidade(possibleValues, tabela)
            if novaSoma != -1:
                # Se a nova solução for melhor ou se um valor entre 0 e 1 for menor que e^(deltaE/t)
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


def experimento(n_execucoes,n_iteracoes,por_tw,termos,saida):
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
    #print(it_certas)
    if acertos_sa != 0:
         it_certas /= acertos_sa
         tem_certas /= acertos_sa
    else:
        it_certas = 0
    #por_hill = (float(acertos_hill) /n_execucoes)*100
    por_sa = (float(acertos_sa) / n_execucoes) * 100
    #tempo_hill/=n_execucoes
    tempo_sim/=n_execucoes
    arq = open(saida,"a")
    arq.write("                                         Dados \n")
    arq.write("Número de execuções: "+ str(n_execucoes)+ "\n")
    arq.write("Número de iterações: " +  str(n_iteracoes) + "\n")
    arq.write("Tempo(em min): " +  str((finish-start)/60) + "\n")
    arq.write("Porcentagem de modificação do tweak:" + str(por_tw*100) + "%\n")
    arq.write("Termos: "+ str(termos) + "\n")
    arq.write("\n                                       Resultado\n")
    arq.write("-----------------------------------------------------------------------------------------------------------\n")
    arq.write("                     |Iterações  | Acertos(em %)| Iterações em acertos |Tempo(em s)| Tempo em acertos(em s)\n")
    # print("-----------------------------------------------------------------")
    # print("Hill Climbing       | {0}      |    {1:.1f}     ||    {2:.3f}".format(res_hill,por_hill,tempo_hill))
    arq.write("------------------------------------------------------------------------------------------------------------\n")
    arq.write("Simulated Annealing  | {0}      |    {1:.1f}     |       {2:.1f}          |    {3:.3f}  |   {4:.3f}         \n".format(res_sa, por_sa, it_certas, tempo_sim, tem_certas))
    arq.write("------------------------------------------------------------------------------------------------------------\n\n")
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
experimento(100, 1000000, 0.3, ["AB","CD", "DA"],"resultado.txt")
experimento(100, 1000000, 0.3, ["SEND","MORE", "MONEY"],"resultado.txt")
experimento(100, 1000000, 0.3, ["POTATO", "TOMATO", "PUMPKIN"],"resultado.txt")
experimento(100, 1000000, 0.3, ["FORTY","TEN","TEN","SIXTY"],"resultado.txt")
#runSimAnnealing(0.3,500000,["FORTY","TEN","TEN","SIXTY"],True)
#print("Lista: ", cria_lista(8))
#print(lista_aleatoria(8,criaTabelaRes(["SEND","MORE", "MONEY"])))
#print(criaTabelaRes(["POTATO", "TOMATO", "PUMPKIN"]))
#["POTATO","TOMATO", "PUMPKIN"]
#["SEND","MORE", "MONEY"]
#["FORTY","TEN","TEN","SIXTY"]
