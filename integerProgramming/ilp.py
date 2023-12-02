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


# Formulation 2: only customers (requirement costs are used in the constraint only)
# Work in progress!
def formulation2():
    instance.transformation1()
    
    model = ConcreteModel()
    model.y = Var(range(instance.m), domain = Binary, initialize = 0)

    model.obj = Objective(
        expr = sum(instance.w[i] * model.y[i] for i in range(instance.m)), sense = maximize
    )
    
    def budget_constraint(model):
        total_cost = 0
        for i in range(instance.n):
            for cus in range(instance.m):
                if value(model.y[cus]) == 1 and i in instance.S[cus]:
                    total_cost += instance.c[i]
                    break
        return total_cost <= instance.b
        #if total_cost == 0: return Constraint.Skip
        #return (None, total_cost, instance.b)

    def budget_constraint2(model):
        total_cost = 0
        added = [0 for _ in range(instance.n)]
        for cus in range(instance.m):
            for i in instance.S[cus]:
                if added[i] == 0:
                    total_cost += instance.c[i] * model.y[cus]
                    added[i] = value(model.y[cus])
        return total_cost <= instance.b

    #model.cons = Constraint(rule = budget_constraint2)
    model.c = Constraint(expr = sum(instance.c[i] for cus in range(instance.m) if value(model.y[cus]) == 1 and i in instance.S[cus] for i in range(instance.n)) <= instance.b)

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit = 1000)
    return model.obj.expr(), results, model


# Formulation 3: only requirements (customers define weight of requirements)
def formulation3():
    model = ConcreteModel()
    model.x = Var(range(instance.n), domain = Binary)

    model.obj = Objective(
        expr = sum(instance.v[i] * model.x[i] for i in range(instance.n)), sense = maximize
    )

    model.cons = ConstraintList()

    model.cons.add(expr = sum(instance.c[i] * model.x[i] for i in range(instance.n)) <= instance.b)

    for pair in instance.P:
        model.cons.add(expr = model.x[pair[0]] >= model.x[pair[1]])

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit = 1000)
    return model.obj.expr(), results, model
    

def solve(formulation):
    if formulation == '1': return formulation1()
    elif formulation == '1t': return formulation1_transformed()
    elif formulation == '2': return formulation2()
    elif formulation == '3': return formulation3()
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
#print(results.solver.status)
#print(results.solver.termination_condition)