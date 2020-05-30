from math import inf
import time
import sys
import tsp
import random

starting_pos = []
def getFirstSolution():
    res = []
    my_pos = 0
    for i, vali in enumerate(matrix):
        for j, valj in enumerate(vali):
            if valj == '5':
                my_pos = [i,j]
                matrix[i] = matrix[i].replace('5','0')
                break
        if(my_pos != 0):
            break
    global starting_pos
    starting_pos = list(my_pos)
    
    while(movePossible(my_pos, 'L')):
        res.append('L')
        my_pos[1]-=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res
        
        
    
    while(movePossible(my_pos, 'D')):
        res.append('D')
        my_pos[0]+=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res
        
        
    
    while(movePossible(my_pos, 'R')):
        res.append('R')
        my_pos[1]+=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res
        
       

    while(movePossible(my_pos, 'U')):
        res.append('U')
        my_pos[0]-=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res
    
    while(movePossible(my_pos, 'L')):
        res.append('L')
        my_pos[1]-=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res

    while(movePossible(my_pos, 'D')):
        res.append('D')
        my_pos[0]+=1
        if(isEndVisible(my_pos) != False):
             res.append(isEndVisible(my_pos))
             return res
        
    return res

def movePossible(pos, move):
    if(move == 'U' and matrix[pos[0] - 1][pos[1]] == '0'): return True
    if(move == 'D' and matrix[pos[0] + 1][pos[1]] == '0'): return True
    if(move == 'L' and matrix[pos[0]][pos[1] - 1] == '0'): return True
    if(move == 'R' and matrix[pos[0]][pos[1] + 1] == '0'): return True

    return False
def isEndVisible(pos):
    if( matrix[pos[0] - 1][pos[1]] == '8'): return 'U'
    if( matrix[pos[0] + 1][pos[1]] == '8'): return 'D'
    if( matrix[pos[0]] [pos[1] - 1] == '8'): return 'L'
    if( matrix[pos[0]] [pos[1] + 1] == '8'): return 'R'
    return False

def generateNeighborhood(candidate):
    res = []
    for i in range(0, len(candidate)):
        for j in range(i, len(candidate)):
            cpy = list(candidate)
            cpy[i] = candidate[j]
            cpy[j] = candidate[i]
            cpy2 = []
            y = 0
            while y < len(cpy)-1:
                if((cpy[y] == 'L' and cpy[y+1]=='R') or (cpy[y] == 'R' and cpy[y+1]=='L') or (cpy[y] == 'U' and cpy[y+1]=='D') or (cpy[y] == 'D' and cpy[y+1]=='U')): 
                    y+=2
                    continue
                else: cpy2.append(cpy[y])
                y+=1
                if(y == len(cpy)-1): cpy2.append(cpy[-1])
            if(cpy2 not in res): res.append(cpy2)
           
    return res



def distanceOfThePath(path):
    global starting_pos
    my_pos = list(starting_pos)
    if(matrix[my_pos[0]][my_pos[1]] == '1'): return inf
    if(matrix[my_pos[0]][my_pos[1]] == '8'): return 0
    for i, step in enumerate(path):
       
        if(step == 'U'): my_pos[0]-=1
        elif (step == 'D'): my_pos[0]+=1
        elif (step == 'R'): my_pos[1]+=1
        elif (step == 'L'): my_pos[1]-=1
        if(matrix[my_pos[0]][my_pos[1]] == '1'): return inf
        if(matrix[my_pos[0]][my_pos[1]] == '8'): return i
        
        
    return inf


def doTabu(maxTabuSize, timeAllowed):
    time1 = time.perf_counter()
    sBest = getFirstSolution()
    bestCandidate = sBest
    tabuList = []
    tabuList.append(sBest)
    i = 0
    while time.perf_counter() - time1 < timeAllowed:      
        sNeighborhood = generateNeighborhood(bestCandidate)
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
    m = int(inp[1])
    matrix = []
    for i in range(int(n)):
        temp = []
        matrix.append(input())
    res = doTabu(1000,t)
    print(len(res))
    for m in res:
        print(m, file=sys.stderr, end ='')    
    #print(getFirstSolution())
    #print(generateNeighborhood(['L', 'D' ,'U']))

    


