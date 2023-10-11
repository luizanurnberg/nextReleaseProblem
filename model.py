from pyomo.environ import *
import instances
import sys

seed = int(sys.argv[1])
value_m = int(sys.argv[2])
instances.generateInstances(seed, value_m)

def solve():

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
    results = solver.solve(model, timelimit=100)
    print(f'\n\nSelected clients')
    for i in range(instances.n):
        print(model.y[i]())

    print(f'\n\nRequirements for the next release')
    for i in range(instances.m):
        print(model.x[i]())

    print(f'\n\nObjective function: {model.obj.expr()}')


solve()