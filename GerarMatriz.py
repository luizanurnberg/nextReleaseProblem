import random
matriz =[]

n = int(input("Informe um valor:"))
m=n
for i in range(n):
    matriz.append([])
    for j in range(m):
        matriz[i].append(random.randint(0,1))

for a in range(n):
    for b in range(m):
        if matriz[a][b]==1 and a!=b:
            matriz[b][a]=-1


for l in matriz:
    print(l)