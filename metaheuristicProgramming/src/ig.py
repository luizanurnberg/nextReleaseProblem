import instance
import sys
import random

def generate_customer_requirements_dict(instance):
    customer_requirements_dict = {}
    for req, cus in instance.Q:
        if cus not in customer_requirements_dict:
            customer_requirements_dict[cus] = {'weight': instance.w[cus], 'requirements': []}
        if req not in customer_requirements_dict[cus]['requirements']:
            customer_requirements_dict[cus]['requirements'].append(req)
    
    return customer_requirements_dict

def select_customer(remaining_customers, customer_requirements_dict, percent_value):
    sorted_customers = sorted(remaining_customers, key=lambda x: customer_requirements_dict[x]['weight'], reverse=True)
    selected_customers_count = max(1, int(percent_value * len(sorted_customers)))
    selected_customers = random.sample(sorted_customers[:selected_customers_count], 1)
    return selected_customers[0]

def can_add(customer, total_cost, added_requirements):
    additional_cost = 0
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 0:
            additional_cost += instance.c[req]
    if total_cost + additional_cost <= instance.b:
        for req in customer_requirements_dict[customer]['requirements']:
            added_requirements[req] += 1
        total_cost += additional_cost
        return True, total_cost
    else:
        return False, total_cost

def can_remove(customer, total_cost, added_requirements):
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 1:
            total_cost -= instance.c[req]
    #if added_requirements[req] > 1:
    for req in customer_requirements_dict[customer]['requirements']:
        added_requirements[req] -= 1
    return True, total_cost
    #else:
    #    return False, total_cost

def heuristic_construction(customer_requirements_dict, solution, k, instance):
    remaining_customers = list(range(instance.m))
    total_cost = 0
    added_requirements = [0 for _ in range(instance.n)]
    obj_value = 0
    selected_customers = []

    while remaining_customers:

        customer = select_customer(remaining_customers, customer_requirements_dict, k)
        remaining_customers.remove(customer)
        can_add_result, total_cost = can_add(customer, total_cost, added_requirements)
        
        if can_add_result:
            solution[customer] = 1
            obj_value += instance.v[customer]
            selected_customers.append(customer)

    for i in range(len(solution)):
        print(f"Customer {i + 1}: Selected = {solution[i]}")

    print('construction', added_requirements)
    heuristic_destruction(customer_requirements_dict, solution, j, instance, added_requirements, total_cost, selected_customers)
    return solution, total_cost, selected_customers
            
def heuristic_destruction(customer_requirements_dict, solution, j, instance, added_requirements, total_cost, selected_customers):
    obj_value = 0

    import math
    d = 0.5
    num_customers_remove = math.ceil(len(selected_customers) * d)


    for _ in range(num_customers_remove):
    #while selected_customers:

        customer = select_customer(selected_customers, customer_requirements_dict, j)
        selected_customers.remove(customer)
        can_remove_result, total_cost = can_remove(customer, total_cost, added_requirements)
        
        if can_remove_result:
            solution[customer] = 2 #deve ser zero
            obj_value += instance.v[customer]

    for i in range(len(solution)):
        print(f"Customer {i + 1}: Selected = {solution[i]}")

    print('destruction', added_requirements)
    return added_requirements

path = sys.argv[1]
factor = float(sys.argv[2])
instance.read(path, factor)
instance.transformation1()
k = float(sys.argv[3]) if len(sys.argv) >= 5 else 0.5
j = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.5

customer_requirements_dict = generate_customer_requirements_dict(instance)
sorted_customers = sorted(customer_requirements_dict.items(), key=lambda x: x[1]['weight'], reverse=True)

for customer, data in sorted_customers:
    requirements = [req + 1 for req in data['requirements']]

num_customers = instance.m
solution = [0] * num_customers # precisamos pegar solução ja semi construida e depois fazer as iterações

solution, total_cost, selected_customers = heuristic_construction(customer_requirements_dict, solution, k, instance)