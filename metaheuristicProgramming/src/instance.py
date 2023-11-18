# Data
n = 0       # number of requirements
m = 0       # number of customers
c = []      # costs of requirements
w = []      # weights/profits of customers
v = []      # weights of requirements given by customers (can be a n x m matrix or a n vector)
P = []      # set of pairs (i,j) where requirement i is a prerequisite of requirement j
Q = []      # set of pairs (i,k) where requirement i is requested by customer k
f = 0       # multiplication factor to compute b
b = 0       # budget
S = []      # set of customers associated with each requirement

def reset():
    global n, m, c, w, v, P, Q, f, b, S
    n = 0
    m = 0
    c = []
    w = []
    v = []
    P = []
    Q = []
    f = 0
    b = 0
    S = []

def read(path, factor):
    global n, m, c, w, v, P, Q, f, b, S
    reset()
    f = factor
    file = open(path, 'r')
    lines = [line.strip() for line in file.readlines()]
    
    levels = int(lines[0])
    line_count = 1
    for _ in range(levels):
        nb_requirements = int(lines[line_count])
        n += nb_requirements
        line_count += 1
        for cost in lines[line_count].split():
            c.append(int(cost))
            v.append(0)
        line_count += 1
    
    dependencies = int(lines[line_count])
    line_count += 1
    for _ in range(dependencies):
        values = lines[line_count].split()
        P.append((int(values[0]) - 1, int(values[1]) - 1))
        line_count += 1
    
    nb_customers = int(lines[line_count])
    m = nb_customers
    line_count += 1
    for customer in range(nb_customers):
        values = [int(value) for value in lines[line_count].split()]
        w.append(values[0])
        for value in values[2:]:
            Q.append((value - 1, customer))
        line_count += 1
    
    b = sum(c) * f
    if b - int(b) == 0.5: b += 0.01
    b = round(b)

    for req, cus in Q:
        v[req] += w[cus]

    for req in range(n):
        S.append([])
        for req2, cus in Q:
            if req == req2: S[-1].append(cus)

def transformation1():
    global n, m, c, w, v, P, Q, f, b, S
    novel = True
    while novel:
        novel = False
        for req, cus in Q:
            for reqi, reqj in P:
                if req == reqj:
                    if (reqi, cus) not in Q:
                        Q.append((reqi, cus))
                        novel = True
    S = []
    for req in range(n):
        S.append([])
        for req2, cus in Q:
            if req == req2: S[-1].append(cus)
