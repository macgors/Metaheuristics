import random
import numpy as np
from math import cos, pi, sqrt
import sys
from random import gauss
import time
from math import inf
from copy import copy

starting_pos = []
def getFirstSolution():
    moves = ['U', 'D', 'L','R']
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
    while( isEndVisible(my_pos) == False):
        next_candidate = random.choice(moves)
        if(movePossible(my_pos,next_candidate)):
            if(next_candidate=='U'): my_pos[0] -=1
            if(next_candidate=='D'): my_pos[0] +=1
            if(next_candidate=='L'): my_pos[1] -=1
            if(next_candidate=='R'): my_pos[1] +=1
            res.append(next_candidate)
    res.append(isEndVisible(my_pos))
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




def annealing(start, cost_function, neighbour, t0, max_time):

    res = start
    cost = cost_function(res)
    t = t0
    start = time.time()
    best_res = res
    best_cost = cost
    while time.time() - start <= max_time:
        t = temperature(t)
        new_res = neighbour(copy(res))
        new_cost = cost_function(new_res)

        if  (new_cost < cost or random.random() < np.exp( (cost - new_cost) / t)):
            res, cost = new_res, new_cost
            if(not new_cost == inf):res = res[0:new_cost]
            if cost <= best_cost:
                best_cost = cost
                best_res = res

    return best_res, best_cost



def random_neighbour(path):
    idx = range(len(path))
    i1, i2 = random.sample(idx, 2)
    path[i1], path[i2] = path[i2], path[i1]
    cpy2 = []
    y = 0
    while y < len(path)-1:
        if((path[y] == 'L' and path[y+1]=='R') or (path[y] == 'R' and path[y+1]=='L') or (path[y] == 'U' and path[y+1]=='D') or (path[y] == 'D' and path[y+1]=='U')): 
            y+=2
            continue
        else: cpy2.append(path[y])
        y+=1
        if(y == len(path)-1): cpy2.append(path[-1])

    return cpy2

def opposite(move):
    if(move == 'U'): return 'D'
    if(move == 'D'): return 'U'
    if(move == 'L'): return 'R'
    if(move == 'R'): return 'L'

def temperature(t):
    return t * 0.99


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
        if(matrix[my_pos[0]][my_pos[1]] == '8'): return i+1
        
        
    return inf




# t0, x1, x2, x3, x4 = map(float, input().split())
# res, cost = annealing((x1,x2,x3,x4), salomon, random_neighbour, 100000, t0)

inp = input().split(' ')
t = float(inp[0])
n = int(inp[1])
m = int(inp[1])
matrix = []
for i in range(int(n)):
    temp = []
    matrix.append(input())

s0 = getFirstSolution()
res,cost = annealing(s0,distanceOfThePath,random_neighbour,10000,t)


print(len(res))
for m in res:
    print(m, file=sys.stderr, end ='')    



