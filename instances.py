import random
import generateDm
import model
import sys

seed = model.seed

n = 5

m = random.randint(1, 10)

v = []
for a in range(n):
    v.append(random.randint(1, 100))

L = 1

c = []
for b in range(m):
    c.append(random.randint(1, 10))

dm = generateDm.generateDm(m)

cm = []
for i in range(n):
    cm.append([])
    for j in range(m):
        cm[i].append(random.randint(0, 1))


def show():
    print()
    print(f'Clientes n= {n}')
    print(f'Requisitos m= {m}')
    print(f'Custo de cada requisito c= {c}')
    print()
    print(f'Limite de custo L= {L}')
    print(f'Peso de importância v= {v}')
    print(f'Matriz de associação de requisitos dm= {dm}')
    print(f'Matriz de associação de clientes:')
    for l in cm:
        print(l)


print("\nValores gerados:")
print(f'n = {n}')
print(f'm = {m}')
print(f'v = {v}')
print(f'L = {L}')
print(f'c = {c}')
print(f'dm = {dm}')
print(f'cm = {cm}')
#  show()
