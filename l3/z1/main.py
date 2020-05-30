import time
from math import log
from random import choice, gauss, random, shuffle, getrandbits,randrange
from math import inf


def yang(xs, eps):
    return sum(e * abs(x) ** (i + 1) for i, (e, x) in enumerate(zip(eps, xs)))


def mutate(xs):
    if(getrandbits(1)): 
       return tuple(x * gauss(1, 0.1) for x in xs)
    else:
        lst = list(xs)
        random_index = randrange(len(lst))
        lst[random_index] = randrange(int(lst[random_index]*2) + 1)
        return tuple(lst)

def mate(a, b):

    random_index = randrange(len(a))
    res1 = list(a)[0:random_index]
    res1.extend(b[random_index:])

    res2 = list(b)[0:random_index]
    res2.extend(a[random_index:])

    return tuple(res1), tuple(res2)


def random_strong_parent(population, eps):
    #draw 5 random potential parents, select strongest of them
    best = choice(population)
    for i in range(1, 5):
        new = choice(population)
        if yang(new,eps) < yang(best,eps):
            best = new
    return best

def genetic(starting_solution, timeout, eps):
    start = time.time()
    popsize = 15
    population = [mutate(starting_solution) for i in range(popsize)]
    best = choice(population)
    best_score = inf


    while time.time() - start < timeout:

        for individual in population:
            if yang(individual,eps) < best_score:
                best = individual
                best_score = yang(individual,eps) 

        next_gen = []
        while len(next_gen) < popsize:
            parent_a = random_strong_parent(population,eps)
            parent_b = random_strong_parent(population,eps)

            kid_a, kid_b = mate(parent_a, parent_b)
            next_gen.append(mutate(kid_a))
            next_gen.append(mutate(kid_b))
        population = next_gen

    return best, best_score


if __name__ == "__main__":
    data = input().split()
    t = float(data[0])
    xs = tuple(map(int, data[1:6]))
    eps = tuple(map(float, data[6:]))


    best, value = genetic(xs,t,eps)

    print(*best, value)
