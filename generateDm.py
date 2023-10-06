import random
import instances

size = instances.m
num_elements = size * size
num_ones = int(0.3 * num_elements)
matrix = [[0 for _ in range(size)] for _ in range(size)]

for _ in range(num_ones):
    while True:
        row = random.randint(0, size - 1)
        column = random.randint(0, size - 1)
        if matrix[row][column] == 0:
            matrix[row][column] = 1
            break

for row in matrix:
    print(row)
