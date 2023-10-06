import random
import generateDm
import sys

n = None

m = None

v = None

L = 100

c = None

dm = None

cm = None


def generate(seed):
    global n, m, v, L, c, dm, cm

    random.seed(seed)

    n = random.randint(1, 10)
    m = random.randint(1, 10)
    v = []
    for a in range(n):
        v.append(random.randint(1, 10))

    c = []
    for b in range(m):
        c.append(random.randint(1, 10))

    dm = generateDm

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

# generate(1)
# show()
