from pyomo.environ import *
import random

def readInstances(instances):

n = 2
m = 2  # randomico tambem
L = 100
v = [random.randint(1, 10) for _ in range(n)]
c = [random.randint(1, 10) for _ in range(m)]
dm = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
cm = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]


def solve():
    model = ConcreteModel()
    model.x = Var(range(m), domain=Binary)
    model.y = Var(range(n), domain=Binary)

    model.obj = Objective(expr=sum(model.y[i] * v[i] for i in range(n)), sense=maximize)

    model.add_component(f'costTotalConstraint-', Constraint(expr=sum(model.x[i] * c[i] for i in range(m)) <= L))

    for i in range(m):
        for j in range(m):
            if dm[i][j] == 1:
                model.add_component(
                    f'reqDependency-{i}-{j}', Constraint(expr=model.x[i] >= model.x[j]))

    for cli in range(n):
        for req in range(m):
            if cm[cli][req] == 1:
                model.add_component(
                    f'reqClientValidity-{cli}-{req}', Constraint(expr=model.x[req] >= model.y[cli]))

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit=100).write()
    print(f'\n\nSelected clients')
    for i in range(n):
        print(model.y[i]())

    print(f'\n\nRequirements for the next release')
    for i in range(m):
        print(model.x[i]())

    print(f'Objective function: {model.obj.expr()}')
