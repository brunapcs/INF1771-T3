import csv
import random
import math
import operator

def leDataSet(arq, split, baseTreino=[] , baseTeste=[]):
    with open(arq, newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(17):
                if (dataset[x][y]) != "?":
                    if y < 11 or y == 17:
                        int(dataset[x][y])
                    if y == 11:
                        if dataset[x][y] == "m":
                            dataset[x][y] = 0
                        else:
                            dataset[x][y] = 1
                    if y == 13 or y == 14 or y == 16:
                        if dataset[x][y] == "yes":
                            dataset[x][y] = 1
                        else:
                            dataset[x][y] = 0
            if random.random() < split:
                baseTreino.append(dataset[x])
            else:
                baseTeste.append(dataset[x])


def calculateDist(instancia1, instancia2, tamanho):
    distancia = 0
    
    for x in range(tamanho-2):
        if( x != 12 and x!= 15):
            if instancia1[x] != "?" and instancia2[x] != "?":
                distancia+= pow((int (instancia1[x]) - int(instancia2[x])), 2)
    return math.sqrt(distancia)


def getvizinhos(baseTreino, instancia, k):
    distancias = []
    tamanho = len(instancia)-1
    for x in range(len(baseTreino)):
        dist = calculateDist(instancia, baseTreino[x], tamanho)
        distancias.append((baseTreino[x], dist))
    distancias.sort(key=operator.itemgetter(1))
    vizinhos = []
    for x in range(k):
        vizinhos.append(distancias[x][0])
    return vizinhos


def classificar(vizinhos):
    votos = {}
    for x in range(len(vizinhos)):
        resp = vizinhos[x][-1]
        if resp in votos:
            votos[resp] += 1
        else:
            votos[resp] = 1
    sortedVotes = sorted(votos.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def acuracia(baseTeste, resultados):
    correto = 0
    for x in range(len(baseTeste)):
        if baseTeste[x][-1] == resultados[x]:
            correto += 1
    return (correto/float(len(baseTeste))) * 100.0


def main():
    # leitura
    baseTreino = []
    baseTeste = []
    split = 0.67
    leDataSet('data.csv', split, baseTreino, baseTeste)
    #  calculos
    resultados = []
    k = 9
    for x in range(len(baseTeste)):
        vizinhos = getvizinhos(baseTreino, baseTeste[x], k)
        result = classificar(vizinhos)
        resultados.append(result)
        print('> obtido=' + repr(result) + ', real=' + repr(baseTeste[x][-1]))
    accuracy = acuracia(baseTeste, resultados)
    print('Acuracia: ' + repr(accuracy) + '%')

main()

