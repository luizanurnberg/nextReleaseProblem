import random

def generateDm(size):
    num_elements = size * size
    num_ones = int(0.2 * num_elements)
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
        c.append(random.randint(1, 10))

    dm = generateDm(m)

    cm = [[0] * m for _ in range(n)]
    for i in range(n):
        j = random.randint(0, m - 1)
        cm[i][j] = 1

    for j in range(m):
        assigned = False
        while not assigned:
            i = random.randint(0, n - 1)
            if cm[i][j] == 0:
                cm[i][j] = 1
                assigned = True

    alpha = 0.9 
    total_cost = sum(c)
    L = alpha * total_cost

    new = '\n'
    print(f'L = {L}\n')
    print(f'v = {v}\n')
    print(f'c = {c}\n')
    print(f'dm = \n{new.join([str(line) for line in dm])}\n')
    print(f'cm = \n{new.join([str(line) for line in cm])}')