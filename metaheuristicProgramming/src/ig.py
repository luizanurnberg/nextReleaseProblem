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
    return customer_requirements_dict

def can_add(customer, total_cost, added_requirements):
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 0:
            total_cost += instance.c[req]
            if total_cost <= instance.b:
                added_requirements[req] += 1
                print("total_cost", total_cost)
                print("instance.b", instance.b)
                return True, total_cost
            else:
                return False, total_cost
    return False, total_cost

def semi_greedy_heuristic(customer_requirements_dict, solution, k, instance):
    remaining_customers = list(range(instance.m))
    total_cost = 0
    added_requirements = [0 for _ in range(instance.n)]

    while len(remaining_customers) > 0:
        customer = random.choice(remaining_customers)
        remaining_customers.remove(customer)
        print("customer", customer)
        
        can_add_result, total_cost = can_add(customer, total_cost, added_requirements)
        
        if can_add_result:
            solution[customer] = 1

    print('req usage count:', added_requirements)
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