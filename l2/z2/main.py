import random
import numpy as np
from math import cos, pi, sqrt
from random import gauss
import sys
import time
from copy import copy

def annealing(M,start, blocks, cost_function, neighbour, t0, max_time):

    res = start
    cost = cost_function(M,res)
    t = t0
    start = time.time()
    best_res = res
    best_cost = cost
    while time.time() - start <= max_time:
        t = temperature(t)
        new_res, new_blocs = neighbour(copy(res), copy(blocks))
        new_cost = cost_function(M,new_res)

        if  (new_cost < cost or random.random() < np.exp( (cost - new_cost) / t)):
            res, cost,blocks = new_res, new_cost,new_blocs
            if cost <= best_cost:
                best_cost = cost
                best_res = res
                


    return best_res, best_cost



def random_neighbour(xs, blocks):
    repainted = random.choice(blocks)
    color = random.choice([0, 32, 64, 128, 160, 192, 223, 255])
    for i in range (repainted[0],repainted[2]+1):
        for j in range(repainted[1],repainted[3]+1):
            xs[i][j] = color
    if(bool(random.getrandbits(1))): return xs,blocks
    if(repainted[1] > 0 and xs[repainted[0]][repainted[1]-1] == color):
        for b in blocks:
            if(b[0]==repainted[0] and b[2]==repainted[2] and b[3]==repainted[3]-1):
                b[3] = repainted[3]
                blocks.delete(repainted)
                break
    elif(repainted[1]>0):
        for b in blocks:
            if(b[0]==repainted[0] and b[2]==repainted[2] and b[3]==repainted[3]-1):
                b[3] +=1
                repainted[1]+=1
                for i in range(repainted[0],repainted[2]):
                    xs[i][b[3]] = xs[b[0]][b[1]]
                break
            
    # if(bool(random.getrandbits(1))):
    #     for b in blocks:
    #         if(b[0]-b[2] > k):

    return xs,blocks

def temperature(t):
    return t * 0.999

def mse_distance(M1, M2):
    n = len(M1)
    m = len(M1[0])
    return sum(sum((M1[i][j] - M2[i][j]) ** 2 for j in range(m)) for i in range(n)) / (n * m)

def first_solution(n,m,k):
    start = np.zeros((n,m), dtype=int)
    
    vals = [0, 32, 64, 128, 160, 192, 223, 255]
    blocks = []
    for i in range(n // k * k):
        for j in range(m // k * k):
            start[i][j] = vals[(i // k + j //k) % len(vals)]
    
    for i in range((n // k) * k, n):
        for j in range(m):
            start[i][j] = start[i-1][j]

    for i in range(n):
        for j in range((m // k) * k, m):
            start[i][j] = start[i][j-1]

    for i in range(0, (n // k) * k,  k ):
        for j in range(0,(m // k) * k ,k):
            blocks.append([i,j])

    for i in blocks:
        if(i[0]+k-1 < n):i.append(i[0]+k-1)
        else:i.append(n)
        if((i[1]+k-1)<m):i.append(i[1]+k-1)
        else: i.append(m)
    return  start, blocks
    



t, n, m, k = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(n)]

# print(matrix)

start, blocks = first_solution(n,m,k)
# print(start)
# print(blocks)

res,cost = annealing(matrix,start,blocks,mse_distance,random_neighbour,100000,10)


print(cost)



# res, cost = annealing((x1,x2,x3,x4), salomon, random_neighbour, 100000, t0)

for i in res:
    for j in i:
        print(j,file=sys.stderr, end =' ')
    print('',file=sys.stderr)
