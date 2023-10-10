import random
import generateDm

def generateInstances(seed, value):
    global n, m, v, L, c, dm, cm

    m = value

    n = 5

    v = []
    for a in range(n):
        v.append(random.randint(1, 10))
    
    c = []
    for b in range(m):
        c.append(random.randint(1, 100))

    dm = generateDm.generateDm(m)

    cm = []
    for i in range(n):
        cm.append([])
        for j in range(m):
            cm[i].append(random.randint(0, 1))

    alpha = 0.5  
    total_cost = sum(c)
    L = alpha * total_cost

    new = '\n'
    print(f'L = {L}\n')
    print(f'v = {v}\n')
    print(f'c = {c}\n')
    print(f'dm = \n{new.join([str(line) for line in dm])}\n')
    print(f'cm = \n{new.join([str(line) for line in cm])}')