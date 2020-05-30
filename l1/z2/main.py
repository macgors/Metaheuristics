from math import inf
import time
import sys
import tsp
import random

def getFirstSolution():
    res = []
    k = 0
    for i in range(0,n-1):
        temp = inf
        for index, val in enumerate(matrix[k]):
            if(val<temp and index not in res and index != 0 and index != k):
                temp = val
                temp_i = index
                k = temp_i
        res.append(temp_i)
    return res

def generateNeighborhood(candidate) -> list:
    res = []
    for i in range(0, len(candidate)):
        for j in range(i, len(candidate)):
            cpy = list(candidate)
            cpy[i] = candidate[j]
            cpy[j] = candidate[i]
            res.append(cpy)
    return res

def generateNeighborhood2(candidate) -> list:
    res = list(range(1,len(candidate)+1))
    random.shuffle(res)
    # for i in range(0, len(candidate)):
    #     for j in range(i, len(candidate)):
    #         cpy = list(candidate)
    #         cpy[i] = candidate[j]
    #         cpy[j] = candidate[i]
    #         r1 = random.randint(0, len(candidate)-1) 
    #         r2 = random.randint(0, len(candidate)-1)
    #         while r1 == r2:
    #              r2 = random.randint(0, len(candidate)-1)
    #         tmp = cpy[r1]
    #         cpy[r1] = cpy[r2]
    #         cpy[r2] = tmp
    #         r1 = random.randint(0, len(candidate)-1) 
    #         r2 = random.randint(0, len(candidate)-1)
    #         while r1 == r2:
    #              r2 = random.randint(0, len(candidate)-1)
    #         tmp = cpy[r1]
    #         cpy[r1] = cpy[r2]
    #         cpy[r2] = tmp
    #         res.append(cpy)
    return [res]

def distanceOfThePath(path):
    res = matrix[0][path[0]] + matrix[path[-1]][0]
    for i in range(len(path) - 1):
        res += matrix[path[i]][path[i+1]]
    return res


def doTabu(maxTabuSize, timeAllowed):
    time1 = time.perf_counter()
    sBest = getFirstSolution()
    bestCandidate = sBest
    tabuList = []
    tabuList.append(sBest)
    i = 0
    while time.perf_counter() - time1 < timeAllowed:
        if i < 1000*timeAllowed: 
            sNeighborhood = generateNeighborhood(bestCandidate)
        else:
             sNeighborhood = generateNeighborhood2(bestCandidate)
        bestCandidate = sNeighborhood[0]
        bestDistance = distanceOfThePath(bestCandidate)
        for sCandidate in sNeighborhood:
            if(sCandidate not in tabuList and distanceOfThePath(sCandidate) < bestDistance):
                bestCandidate = sCandidate
                bestDistance = distanceOfThePath(bestCandidate)
        
        if(distanceOfThePath(bestCandidate) < distanceOfThePath(sBest)):
            sBest = bestCandidate
            i = 0
        tabuList.append(bestCandidate)
        if(len(tabuList) > maxTabuSize):
            tabuList.pop(0)
        i+=1
    return sBest


if __name__ == "__main__":
    inp = input().split(' ')
    t = float(inp[0])
    n = int(inp[1])
    matrix = []
    for i in range(int(n)):
        temp = []
        for j in input().split(' '):
            temp.append(int(j))
        matrix.append(temp)

    res = doTabu(inf,t)
    print(distanceOfThePath(res))
    print("1", file=sys.stderr, end =' ')
    for i in res:
        print(i+1, file=sys.stderr, end =' ')
    print("1", file=sys.stderr, end =' ')    



