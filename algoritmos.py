# -*- coding: utf-8
# Stephen Marsland, 2008, 2014
# Adaptação e correção de bugs por Hendrik Macedo, 2017


import numpy as np
import time


def makeTSP(nCities):
    # positions corresponde às coordenadas de cada uma das n cidades
    # positions é uma matriz n X 2, onde n é o número de cidades
    # np.random.rand(n,m) retorna uma matriz n x m de valores aleatórios entre 0.0 e 1.0
    positions = 2 * np.random.rand(nCities, 2) - 1;
    # distances corresponde às distâncias entre cada cidade
    # distances é uma matriz n x n
    # a matriz é inicializada
    distances = np.zeros((nCities, nCities))

    # os valores das distâncias são calculados
    for i in range(nCities):
        for j in range(i + 1, nCities):
            distances[i, j] = np.sqrt(
                (positions[i, 0] - positions[j, 0]) ** 2 + (positions[i, 1] - positions[j, 1]) ** 2);
            distances[j, i] = distances[i, j];

    return distances


def permutation(order):
    order = tuple(order)
    if len(order) == 1:
        yield order
    else:
        for i in range(len(order)):
            rest = order[:i] + order[i + 1:]
            move = (order[i],)
            for smaller in permutation(rest):
                yield move + smaller


def greedy(distances):
    nCities = np.shape(distances)[0]
    distanceTravelled = 0

    # Need a version of the matrix we can trash
    dist = distances.copy()

    cityOrder = np.zeros(nCities, dtype=int)
    cityOrder[0] = np.random.randint(nCities)
    dist[:, int(cityOrder[0])] = np.Inf

    for i in range(nCities - 1):
        cityOrder[i + 1] = np.argmin(dist[cityOrder[i], :])
        distanceTravelled += dist[cityOrder[i], cityOrder[i + 1]]
        # Now exclude the chance of travelling to that city again
        dist[:, cityOrder[i + 1]] = np.Inf

    # Now return to the original city
    distanceTravelled += distances[cityOrder[nCities - 1], 0]

    return cityOrder, distanceTravelled


def hillClimbing(distances):
    # np.shape(v) retorna um vetor que corresponde à dimensão da matriz v

    nCities = np.shape(distances)[0]

    # np.arange(n) retorna um vetor com de tamanho n com a sequência de 0 a n-1
    cityOrder = np.arange(nCities)

    # np.shuffle(v) bagunça os elementos de v
    np.random.shuffle(cityOrder)

    distanceTravelled = 0
    for i in range(nCities - 1):
        distanceTravelled += distances[cityOrder[i], cityOrder[i + 1]]
    distanceTravelled += distances[cityOrder[nCities - 1], 0]

    for i in range(1000):
        # Choose cities to swap
        city1 = np.random.randint(nCities)
        city2 = np.random.randint(nCities)

        if city1 != city2:
            # Reorder the set of cities
            possibleCityOrder = cityOrder.copy()
            possibleCityOrder = np.where(possibleCityOrder == city1, -1, possibleCityOrder)
            possibleCityOrder = np.where(possibleCityOrder == city2, city1, possibleCityOrder)
            possibleCityOrder = np.where(possibleCityOrder == -1, city2, possibleCityOrder)

            # Work out the new distances
            # This can be done more efficiently
            newDistanceTravelled = 0
            for j in range(nCities - 1):
                newDistanceTravelled += distances[possibleCityOrder[j], possibleCityOrder[j + 1]]
            distanceTravelled += distances[cityOrder[nCities - 1], 0]

            if newDistanceTravelled < distanceTravelled:
                distanceTravelled = newDistanceTravelled
                cityOrder = possibleCityOrder

    return cityOrder, distanceTravelled


def simulatedAnnealing(distances):
    nCities = np.shape(distances)[0]

    cityOrder = np.arange(nCities)
    np.random.shuffle(cityOrder)

    distanceTravelled = 0
    for i in range(nCities - 1):
        distanceTravelled += distances[cityOrder[i], cityOrder[i + 1]]
    distanceTravelled += distances[cityOrder[nCities - 1], 0]

    T = 500
    c = 0.8
    nTests = 1000

    # while T>1:
    for i in range(nTests):
        # Choose cities to swap
        city1 = np.random.randint(nCities)
        city2 = np.random.randint(nCities)

        if city1 != city2:
            # Reorder the set of cities
            possibleCityOrder = cityOrder.copy()
            possibleCityOrder = np.where(possibleCityOrder == city1, -1, possibleCityOrder)
            possibleCityOrder = np.where(possibleCityOrder == city2, city1, possibleCityOrder)
            possibleCityOrder = np.where(possibleCityOrder == -1, city2, possibleCityOrder)

            # Work out the new distances
            # This can be done more efficiently
            newDistanceTravelled = 0
            for j in range(nCities - 1):
                newDistanceTravelled += distances[possibleCityOrder[j], possibleCityOrder[j + 1]]
            distanceTravelled += distances[cityOrder[nCities - 1], 0]

            if (newDistanceTravelled < distanceTravelled) or (
                (distanceTravelled - newDistanceTravelled) > T * np.log(np.random.rand())):
                distanceTravelled = newDistanceTravelled
                cityOrder = possibleCityOrder

        # Annealing schedule
        T = c * T

    return cityOrder, distanceTravelled


def parameters(nCities):
    #	import time
    #	nCities = ncities
    distances = makeTSP(nCities)
    return distances


def runExaustive(distances):
    print("Busca exaustiva")
    start = time.time()
    result = exhaustive(distances)
    finish = time.time()
    print("Ordem:", result[0], " Distancia:", result[1])
    print("Tempo:", finish - start)


def runGreedy(distances):
    print("\nGreedy")
    start = time.time()
    result = greedy(distances)
    finish = time.time()
    print("Ordem:", result[0], " Distancia:", result[1])
    print("Tempo:", finish - start)


def runHill(distances):
    print("\nHill Climbing")
    start = time.time()
    result = hillClimbing(distances)
    finish = time.time()
    print("Ordem:", result[0], " Distancia:", result[1])
    print("Tempo:", finish - start)


def runSimAnnealing(distances):
    print("\nSimulated Annealing")
    start = time.time()
    result = simulatedAnnealing(distances)
    finish = time.time()
    print("Ordem:", result[0], " Distancia:", result[1])
    print("Tempo:", finish - start)