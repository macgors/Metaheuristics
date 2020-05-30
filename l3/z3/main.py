import time
from random import choice, gauss, random, shuffle, getrandbits,randrange
from math import inf
from copy import deepcopy
import sys

starting_pos = []
def get_position():
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


def fittnes(path):
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

def mutate(path):
    i = randrange(len(path))
    j = randrange(len(path))
    path[i], path[j] = path[j], path[i]
    # cpy2 = []
    # y = 0
    # while y < len(path)-1:
    #     if((path[y] == 'L' and path[y+1]=='R') or (path[y] == 'R' and path[y+1]=='L') or (path[y] == 'U' and path[y+1]=='D') or (path[y] == 'D' and path[y+1]=='U')): 
    #         y+=2
    #         continue
    #     else: cpy2.append(path[y])
    #     y+=1
    #     if(y == len(path)-1): cpy2.append(path[-1])
    # return cpy2
    return path
    


def mate(a, b):

    random_index = randrange(len(a))
    res1 = a[0:random_index]
    res1 += b[random_index:]

    res2 = b[0:random_index]
    res2 += a[random_index:]

    return res1, res2
    #     parents = set(a + b)
    # kid = list(parents)
    # kid_a = deepcopy(kid)
    # shuffle(kid)
    # shuffle(kid_a)
 
    # return ''.join(kid_a[:len(a)]), ''.join(kid[:len(a)])


def random_strong_parent(population):
    #draw x random potential parents, select strongest of them
    best = choice(population)
    for i in range(1, 4):
        new = choice(population)
        if fittnes(new) < fittnes(best):
            best = new
    return best

def genetic(starting_solutions, timeout, p):
    start = time.time()
    popsize = p
    if(popsize < len(starting_solutions)): popsize = len(starting_solutions)
    population = starting_solutions
    best = choice(population)
    best_score = fittnes(best)


    while time.time() - start < timeout:

        for individual in population:
            if fittnes(individual) < best_score:
                best = individual
                best_score = fittnes(individual) 

        next_gen = []

        while len(next_gen) < popsize:
            parent_a = random_strong_parent(population)
            parent_b = random_strong_parent(population)
           
            kid_a, kid_b = mate(parent_a, parent_b)
            next_gen.append(mutate(kid_a))
            next_gen.append(mutate(kid_b))
        population = next_gen


    return best, best_score


if __name__ == "__main__":
    
    t, n, m, s, p = map(int, input().split())

    matrix = []
    for i in range(int(n)):
        matrix.append(input())

    initial_candidates = []
    for i in range(s):
        initial_candidates.append(list(input()))
    get_position()


    best, score = genetic(initial_candidates,t, p)
    
    print(score)
    for m in best[0:score]:
        print(m, file=sys.stderr, end ='')    
