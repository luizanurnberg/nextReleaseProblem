import random
import generateDm

def generateInstances(seed, value):
    global n, m, v, L, c, dm, cm

    m= value

    n = 5

    v = []
    for a in range(n):
        v.append(random.randint(1, 10))

    L = 100
    
    c = []
    for b in range(m):
        c.append(random.randint(1, 100))

    dm = generateDm.generateDm(m)

    cm = []
    for i in range(n):
        cm.append([])
        for j in range(m):
            cm[i].append(random.randint(0, 1))

    print(f'v = {v}')
    print(f'c = {c}')
    print(f'dm = {dm}')
    print(f'cm = {cm}')
