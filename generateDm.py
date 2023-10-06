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
