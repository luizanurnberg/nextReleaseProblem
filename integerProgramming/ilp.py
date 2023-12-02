from pyomo.environ import *
import instance
import sys

formulation = 1

def solution(model):
    result = 'Customers:'
    for i in range(instance.m):
        if model.y[i]() == 1: result += ' ' + str(i + 1)
    result += '; Requirements:'
    for i in range(instance.n):
        if model.x[i]() == 1: result += ' ' + str(i + 1)
    return result

# Formulation 1: general
def formulation1():
    model = ConcreteModel()
    model.x = Var(range(instance.n), domain = Binary)
    model.y = Var(range(instance.m), domain = Binary)

    model.obj = Objective(
        expr = sum(instance.w[i] * model.y[i] for i in range(instance.m)), sense = maximize
    )

    model.cons = ConstraintList()

    model.cons.add(expr = sum(instance.c[i] * model.x[i] for i in range(instance.n)) <= instance.b)

    for pair in instance.P:
        model.cons.add(expr = model.x[pair[0]] >= model.x[pair[1]])

    for pair in instance.Q:
        model.cons.add(expr = model.x[pair[0]] >= model.y[pair[1]])

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit = 1000)
    return model.obj.expr(), results, model


# Formulation 1 transformed: general + transformation to remove requirements dependency
def formulation1_transformed():
    instance.transformation1()

    model = ConcreteModel()
    model.x = Var(range(instance.n), domain = Binary)
    model.y = Var(range(instance.m), domain = Binary)

    model.obj = Objective(
        expr = sum(instance.w[i] * model.y[i] for i in range(instance.m)), sense = maximize
    )

    model.cons = ConstraintList()

    model.cons.add(expr = sum(instance.c[i] * model.x[i] for i in range(instance.n)) <= instance.b)

    for pair in instance.Q:
        model.cons.add(expr = model.x[pair[0]] >= model.y[pair[1]])

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit = 1000)
    return model.obj.expr(), results, model

def solve(formulation):
    if formulation == '1': return formulation1()
    elif formulation == '1t': return formulation1_transformed()
    print(f'Invalid formulation: {formulation}')
    exit()


if len(sys.argv) < 3:
    print('Usage: ilp.py <path> <factor> [<formulation>]')
    exit()

path = sys.argv[1]
factor = float(sys.argv[2])
formulation = sys.argv[3] if len(sys.argv) >= 4 else '1'
instance.read(path, factor)
value, results, model = solve(formulation)
print(value)
if results.solver.termination_condition != TerminationCondition.optimal: print(results.solver.termination_condition)