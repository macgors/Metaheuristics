import time
from random import choice, gauss, random, shuffle, getrandbits,randrange
from math import inf
from copy import deepcopy
import sys


def fittnes(s,dictionary,points):
    points = deepcopy(points)
    res = 0
    for c in s:
        if(len(points[c]) != 0):
            res += points[c].pop()
        else: return -1
    if(s not in dictionary): return 0
    return res



def mutate(s, dictionary, points):
    points = deepcopy(points)
    for c in s:
        if(len(points[c]) != 0):
            points[c].pop()
            if(points[c] == 0): del points[c]
    letters = list(points.keys())
    r = random()
    if(r < 0.03 and len(s) < 9):
        return s + choice(letters)
    if(r < 0.20):
        s = list(s)
        random_index = randrange(len(s))
        s[random_index] = choice(letters)
        return ''.join(s)
    if(r < 0.22 and len(s) > 5):
        return s[:-1]
    else:
        l = list(s)
        shuffle(l)
        return ''.join(l)
    


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


def random_strong_parent(population, dictionary, points):
    #draw x random potential parents, select strongest of them
    best = choice(population)
    for i in range(1, 4):
        new = choice(population)
        if fittnes(new,dictionary,points) > fittnes(best,dictionary,points):
            best = new
    return best

def genetic(starting_solutions, timeout, dictionary, points):
    start = time.time()
    popsize = 10
    if(popsize < len(starting_solutions)): popsize = len(starting_solutions)
    population = starting_solutions
    best = choice(population)
    best_score = fittnes(best,dictionary,points)


    while time.time() - start < timeout:

        for individual in population:
            if fittnes(individual,dictionary,points) > best_score:
                best = individual
                best_score = fittnes(individual,dictionary,points) 

        next_gen = []
        used_parents = []
        while len(next_gen) < popsize:
            parent_a = random_strong_parent(population,dictionary, points)
            parent_b = random_strong_parent(population,dictionary, points)
            if(parent_a in used_parents or parent_b in used_parents): continue
            kid_a, kid_b = mate(parent_a, parent_b)
            next_gen.append(mutate(kid_a, dictionary,points))
            next_gen.append(mutate(kid_b, dictionary,points))
        population = next_gen
        #print(population)

    return best, best_score


if __name__ == "__main__":
    t, n, s = map(int, input().split())

    points = {}
    for _ in range(n):
        c,val = input().split()
        if(c in points):
            points[c].append(int(val))
        else: points[c] = [int(val)]

    starting_solution = []
    for _ in range(s):
        starting_solution.append(input())

    
    with open("dict.txt", "r") as f:
        words = f.readlines()
        dictionary = []
        for word in words:
            dictionary.append(word[:-1].lower())

    #print(points)
    #print(starting_solution)

    #print(fittnes('bean',dictionary,points))
    word, score = genetic(starting_solution,t,dictionary,points)
    print(score)
    print(word, file=sys.stderr) 