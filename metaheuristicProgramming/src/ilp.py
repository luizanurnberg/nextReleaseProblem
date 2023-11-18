from pyomo.environ import *
import instance
import sys
import random

formulation = 1

def solution(model):
    result = 'Customers:'
    for i in range(instance.m):
        if model.y[i]() == 1: result += ' ' + str(i + 1)
    result += '; Requirements:'
    for i in range(instance.n):
        if model.x[i]() == 1: result += ' ' + str(i + 1)
    return result

# Formulation 1 transformed: general + transformation to remove requirements dependency
def formulation1_transformed():
    instance.transformation1()

    model = ConcreteModel()
    model.x = Var(range(instance.n), domain=Binary)
    model.y = Var(range(instance.m), domain=Binary)

    model.obj = Objective(
        expr=sum(instance.w[i] * model.y[i] for i in range(instance.m)), sense=maximize
    )

    model.cons = ConstraintList()

    model.cons.add(expr=sum(instance.c[i] * model.x[i] for i in range(instance.n)) <= instance.b)

    for pair in instance.Q:
        model.cons.add(expr=model.x[pair[0]] >= model.y[pair[1]])

    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit=1000)
    return model.obj.expr(), results, model

def solve(formulation):
    if formulation == '1t': return formulation1_transformed()
    print(f'Invalid formulation: {formulation}')
    exit()

path = sys.argv[1]
factor = float(sys.argv[2])
formulation = sys.argv[3] if len(sys.argv) >= 4 else '1'
instance.read(path, factor)
value, results, model = solve(formulation)
print(value)

if results.solver.termination_condition != TerminationCondition.optimal: print(results.solver.termination_condition)
print(results.solver.status)
print(results.solver.termination_condition)

#--------------Created Client's Dictionary With Requirements-----------------
def generate_customer_requirements_dict(instance):
    customer_requirements_dict = {}

    for req, cus in instance.Q:
        if cus not in customer_requirements_dict:
            customer_requirements_dict[cus] = {'weight': instance.w[cus], 'requirements': [], 'dependencies': []}

        if req not in customer_requirements_dict[cus]['requirements']:
            customer_requirements_dict[cus]['requirements'].append(req)

        for reqi, reqj in instance.P:
            if req == reqj:
                if reqi not in customer_requirements_dict[cus]['requirements']:
                    customer_requirements_dict[cus]['requirements'].append(reqi)

                if reqi != reqj:
                    customer_requirements_dict[cus]['dependencies'].append((reqi, reqj))

    return customer_requirements_dict

customer_requirements_dict = generate_customer_requirements_dict(instance)

sorted_customers = sorted(customer_requirements_dict.items(), key=lambda x: x[1]['weight'], reverse=True)

for customer, data in sorted_customers:
    requirements = [req + 1 for req in data['requirements']]
    dependencies = [(dep[0] + 1, dep[1] + 1) for dep in data['dependencies']]

    print(f"Customer {customer + 1}: Weight {data['weight']}, Requirements {requirements}")

    # if dependencies:
    #     print(f"Dependencies:")
    #     for dep in dependencies:
    #         print(f"  Requirement {dep[0]} depends on Requirement {dep[1]}")

#----------------Created client's binary vector-----------------
num_customers = instance.m
customer_vector = [0] * num_customers

#-----------------Created semi-greedy heuristic---------------------------
def semi_greedy_heuristic(customer_requirements_dict, customer_vector, k, instance):
    num_customers = len(customer_vector)
    num_selected_customers = int(k * num_customers)

    shuffled_customers = list(range(num_customers))
    random.shuffle(shuffled_customers)

    total_weight = 0
    selected_requirements_weights = []

    for customer_idx in shuffled_customers:
        customer_data = customer_requirements_dict[customer_idx]
        customer_requirements = customer_data['requirements']

        customer_weight = 0
        selected_requirements = []

        for req in customer_requirements:
            req_weight = instance.c[req - 1]
            customer_weight += req_weight
            selected_requirements.append((req, req_weight))

        # print("Client selected:", customer_idx)
        # print("Requirements selected:", selected_requirements)
        # print("Requirement's weight:", customer_weight)

        if total_weight + customer_weight <= instance.b:
            customer_vector[customer_idx] = 1
            total_weight += customer_weight
            selected_requirements_weights.extend(selected_requirements)

    return total_weight, selected_requirements_weights

k = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.5

total_cost, selected_weights = semi_greedy_heuristic(customer_requirements_dict, customer_vector, k, instance)

print("Budget:", instance.b)
print("Total cost:", total_cost)
