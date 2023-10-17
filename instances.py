import random
from math import floor, ceil

def generateDm(size):
    
    if size < 200:
        parent_probability = 0.2
        level_density = [0.6, 0.2, 0.15, 0.05]
    elif size >= 200:
        parent_probability = 0.01
        level_density = [0.5, 0.3, 0.15, 0.05]

    level_nodes = [[] for _ in range(len(level_density))]

    level_amount = []
    for density in level_density:
        level_amount.append(floor(density * m))
    level_amount[-1] += m - sum(level_amount)

    nodes = [x for x in range(m)]

    level = 0
    for amount in level_amount:
        for _ in range(amount):
            node = random.choice(nodes)
            nodes.remove(node)
            level_nodes[level].append(node)
        level += 1

    matrix = [[0 for _ in range(m)] for _ in range(m)]
    for level in range(3, 0, -1):
        for node in level_nodes[level]:
            for parent_node in level_nodes[level - 1]:
                if random.random() < parent_probability:
                    matrix[parent_node][node] = 1

    return matrix

def generateInstances(seed, value_n, value_m):
    global n, m, v, L, c, dm, cm

    random.seed(seed)

    n = value_n

    m = value_m

    v = []
    for a in range(n):
        v.append(random.randint(1, 10))

    c = []
    for b in range(m):
        c.append(random.randint(1, 10))

    dm = generateDm(m)

    cm = [[0] * m for _ in range(n)]
    cm_density = 0.1
    for i in range(n):
        for _ in range(ceil(m * cm_density)):
            j = random.randint(0, m - 1)
            cm[i][j] = 1

    for j in range(m):
        all_zero = True
        for i in range(n):
            if cm[i][j] == 1:
                all_zero = False
                break
        if all_zero:
            i = random.randint(0, n - 1)
            cm[i][j] = 1

    alpha = 0.4
    total_cost = sum(c)
    L = alpha * total_cost
    L = round(L, 2)

    new = '\n'
    print(f'L = {L}\n')
    print(f'v = {v}\n')
    print(f'c = {c}\n')
    print(f'dm = \n{new.join([str(line) for line in dm])}\n')
    print(f'cm = \n{new.join([str(line) for line in cm])}')