import generateDm
from pyomo.environ import *
import instances
import sys

seed = int(sys.argv[1])

n = None
m = None
v = None
L = 100
c = None
dm = None
cm = None


def read_instances(filename):
    global n, m, v, L, c, dm, cm

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            n, m = map(int, lines[0].split())
            v = list(map(int, lines[1].split()))
            c = list(map(int, lines[2].split()))
            L = int(lines[3])
            dm = generateDm
            cm = []
            for line in lines[4:]:
                cm.append(list(map(int, line.split())))

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def solve():

    instances.generate(seed)

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
    results = solver.solve(model, timelimit=100).write()
    print(f'\n\nSelected clients')
    for i in range(instances.n):
        print(model.y[i]())

    print(f'\n\nRequirements for the next release')
    for i in range(instances.m):
        print(model.x[i]())

    print(f'Objective function: {model.obj.expr()}')


modelInstances = instances.generate(seed)
read_instances(modelInstances)
print(solve())
