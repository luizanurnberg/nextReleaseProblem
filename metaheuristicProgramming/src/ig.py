import instance
import sys
import random

#--------------Created Client's Dictionary With Requirements-----------------
def generate_customer_requirements_dict(instance):
    customer_requirements_dict = {}
    for req, cus in instance.Q:
        if cus not in customer_requirements_dict:
            customer_requirements_dict[cus] = {'weight': instance.w[cus], 'requirements': []}
        if req not in customer_requirements_dict[cus]['requirements']:
            customer_requirements_dict[cus]['requirements'].append(req)
    
    for customer, data in customer_requirements_dict.items():
        print(f"Customer: {customer}")
        print(f"Weight: {data['weight']}")
        print(f"Requirements: {data['requirements']}")
        print("\n")
    
    return customer_requirements_dict

def can_add(customer, total_cost, added_requirements):
    additional_cost = 0
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 0:
            additional_cost += instance.c[req]
    if total_cost + additional_cost <= instance.b:
        for req in customer_requirements_dict[customer]['requirements']:
            added_requirements[req] += 1
        print("total_cost", total_cost)
        print("instance.b", instance.b)
        total_cost += additional_cost
        return True, total_cost
    else:
        return False, total_cost

def select_customer(remaining_customers, customer_requirements_dict, k):
    sorted_customers = sorted(remaining_customers, key=lambda x: customer_requirements_dict[x]['weight'], reverse=True)

    selected_customers_count = max(1, int(k * len(sorted_customers)))
    selected_customers = random.sample(sorted_customers[:selected_customers_count], 1)
    print("selected_customers", selected_customers)
    return selected_customers[0]

def semi_greedy_heuristic(customer_requirements_dict, solution, k, instance):
    remaining_customers = list(range(instance.m))
    total_cost = 0
    added_requirements = [0 for _ in range(instance.n)]
    obj_value = 0

    while remaining_customers:

        customer = select_customer(remaining_customers, customer_requirements_dict, k)
        remaining_customers.remove(customer)
        
        can_add_result, total_cost = can_add(customer, total_cost, added_requirements)
        
        if can_add_result:
            solution[customer] = 1
            obj_value += instance.v[customer]

    print('req usage count:', added_requirements)
    print('obj value:', obj_value)
    for i in range(len(solution)):
        print(f"Customer {i + 1}: Selected = {solution[i]}")

    selected_requirements = [i for i, count in enumerate(added_requirements) if count > 0]
    print('Selected Requirements:', selected_requirements)
    return solution, total_cost

path = sys.argv[1]
factor = float(sys.argv[2])
instance.read(path, factor)
instance.transformation1()
k = float(sys.argv[3]) if len(sys.argv) >= 5 else 0.5

customer_requirements_dict = generate_customer_requirements_dict(instance)
sorted_customers = sorted(customer_requirements_dict.items(), key=lambda x: x[1]['weight'], reverse=True)

for customer, data in sorted_customers:
    requirements = [req + 1 for req in data['requirements']]
    #print(f"Customer {customer + 1}: Weight {data['weight']}, Requirements {requirements}")

#----------------Created client binary vector-----------------
num_customers = instance.m
solution = [0] * num_customers

#total_cost, selected_weights = semi_greedy_heuristic(customer_requirements_dict, solution, k, instance)
solution, total_cost = semi_greedy_heuristic(customer_requirements_dict, solution, k, instance)

# print('total cost:', total_cost)
# print('solution:', solution)