from random import random
import numpy as np
from math import cos, pi, sqrt
from random import gauss
import time
from copy import copy

def annealing(start, cost_function, neighbour, t0, max_time):

    res = start
    cost = cost_function(res)
    t = t0
    start = time.time()
    #####
    best_res = res
    best_cost = cost
    #####
    while time.time() - start <= max_time:
        t = temperature(t)
        new_res = neighbour(res)
        new_cost = cost_function(new_res)

        if  (new_cost < cost or random() < np.exp( - (cost - new_cost) / t)):
            res, cost = new_res, new_cost
            #####
            if cost <= best_cost:
                best_cost = cost
                best_res = res
            #####

    return best_res, best_cost


def salomon(xs):
    sqrt_sum = sqrt(sum(x ** 2 for x in xs))
    return 1 - cos(2 * pi * sqrt_sum) + 0.1 * sqrt_sum

def random_neighbour(xs):
    return tuple(x * gauss(1, 0.1) for x in xs)

def temperature(t):
    return t * 0.999


t0, x1, x2, x3, x4 = map(float, input().split())
res, cost = annealing((x1,x2,x3,x4), salomon, random_neighbour, 100000, t0)

for i in res:
    print(i, end =' ')
print(cost)