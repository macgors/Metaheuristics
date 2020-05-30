import math
import random
import time

def norm(vector):
    return math.sqrt(sum(x ** 2 for x in vector))

def griewank(vector):
    return 1.0 + sum(((x ** 2) / 4000.0) for x in vector) - prod((math.cos(x / (i + 1)) for i, x in enumerate(vector)))

def happy_cat(vector):
    return ((norm(vector) ** 2 - 4) ** 2) ** (0.125) + 0.25 * (0.5 * norm(vector) ** 2 + sum(vector)) + 0.5

def prod(x):
    res = 1
    for i in x:
        res*=i
    return res 
#Hill-Climbing with Random Restarts from
# Essentials of Metaheuristics
# A Set of Undergraduate Lecture Notes by
# Sean Luke
# Department of Computer Science
# George Mason University
def solve(function, timeout):
    s = list(random.gauss(0, 1) for i in range(4))
    best = s

    start = time.time()
    while time.time() - start < timeout:
        t = abs(random.random())*timeout

        start_2nd = time.time()
        while time.time() - start_2nd < t and time.time() - start < timeout:
            r = list(x + random.gauss(0, sigma) for x in s)
            if function(r) < function(s):
                s = r

        if function(s) <= function(best):
            best = s

        s = list(random.gauss(0, sigma) for i in range(4))

    return (best)


if __name__ == "__main__":
    inp = input().split(' ')
    t = float(inp[0])
    b = inp[1]
    if(b == '0'): 
        sigma = 0.001
        res = solve(happy_cat,t)
        resY = happy_cat(res)
    if(b == '1'): 
        sigma = 0.0000001
        res= solve(griewank,t)
        resY = griewank(res)
    for i in res:
        print(i, end=' ')
    print(resY)
    