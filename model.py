from pyomo.environ import *
import time
import instances
import sys

if len(sys.argv) != 4:
    print("Para executar: passar 'py model.py seed n m' onde seed é a semente, n é a quantidade de clientes e m é a quantidade de requisitos")
    sys.exit(1)

seed = int(sys.argv[1])
value_n = int(sys.argv[2])
value_m = int(sys.argv[3])
instances.generateInstances(seed, value_n, value_m)

def solve():
    start_time = time.time()

    model = ConcreteModel()
    model.x = Var(range(instances.m), domain=Binary)
    model.y = Var(range(instances.n), domain=Binary)

    model.obj = Objective(expr=sum(
        model.y[i] * instances.v[i] for i in range(instances.n)), sense=maximize)

    model.add_component(f'costTotalConstraint-', Constraint(expr=sum(
        model.x[i] * instances.c[i] for i in range(instances.m)) <= instances.L))

    for i in range(instances.m):
        for j in range(instances.m):
            if instances.dm[i][j] == 1:
                model.add_component(
                    f'reqDependency-{i}-{j}', Constraint(expr=model.x[i] >= model.x[j]))

    for cli in range(instances.n):
        for req in range(instances.m):
            if instances.cm[cli][req] == 1:
                model.add_component(
                    f'reqClientValidity-{cli}-{req}', Constraint(expr=model.x[req] >= model.y[cli]))

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit=200)

    print(f'\n\nRequirements for the next release')
    for i in range(instances.m):
        print(f'{i + 1}° Requirement: {model.x[i]()}')

    print(f'\n\nSelected clients')
    for i in range(instances.n):
        print(f'{i + 1}° Client: {model.y[i]()}')

    print(f'\n\nObjective function: {model.obj.expr()}')

    end_time = time.time()
    execution_time = end_time - start_time

    print(f'Seed: {seed}')
    print(f'Quantidade de requisitos: {instances.m}')
    print(f'Quantidade de clientes: {instances.n}')
    print(f"Tempo de execução: {execution_time} segundos")

solve()

if name == "main":
    solve()