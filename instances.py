import random

def generateDm(size):
    num_elements = size * size
    num_ones = int(0.3 * num_elements)
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    def is_valid_position(row, column):
        neighbors = [(row-1, column), (row+1, column),
                    (row, column-1), (row, column+1)]
        for r, c in neighbors:
            if 0 <= r < size and 0 <= c < size and matrix[r][c] == 1:
                return False
        return True

    for i in range(num_ones):
        while True:
            row = random.randint(0, size - 1)
            column = random.randint(0, size - 1)
            if matrix[row][column] == 0 and is_valid_position(row, column) and row != column:
                matrix[row][column] = 1
                break

    for i in range(size):
        matrix[i][i] = 0

    return matrix

def generateInstances(seed, value):
    global n, m, v, L, c, dm, cm

    random.seed(seed)

    m = value

    n = 5

    v = []
    for a in range(n):
        v.append(random.randint(1, 10))
    
    c = []
    for b in range(m):
        c.append(random.randint(1, 100))

    dm = generateDm(m)

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