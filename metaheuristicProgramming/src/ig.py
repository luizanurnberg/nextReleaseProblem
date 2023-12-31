import instance
import sys
import random
import math
import time

# random.seed(5)


def generate_customer_requirements_dict(instance):
    customer_requirements_dict = {}
    for req, cus in instance.Q:
        if cus not in customer_requirements_dict:
            customer_requirements_dict[cus] = {
                'weight': instance.w[cus], 'requirements': []}
        if req not in customer_requirements_dict[cus]['requirements']:
            customer_requirements_dict[cus]['requirements'].append(req)
    return customer_requirements_dict


def select_customer(remaining_customers, customer_requirements_dict, percent_value, reverse=True):
    sorted_customers = sorted(
        remaining_customers, key=lambda x: customer_requirements_dict[x]['weight'], reverse=reverse)
    amount = max(1, int(percent_value * len(sorted_customers)))
    sample = random.sample(sorted_customers[:amount], 1)
    return sample[0]


def can_add(customer, total_cost, added_requirements):
    additional_cost = 0
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 0:
            additional_cost += instance.c[req]

    if total_cost + additional_cost <= instance.b:
        for req in customer_requirements_dict[customer]['requirements']:
            added_requirements[req] += 1
        total_cost += additional_cost
        return True, total_cost, added_requirements
    else:
        return False, total_cost, added_requirements


def can_remove(customer, total_cost, added_requirements):
    for req in customer_requirements_dict[customer]['requirements']:
        if added_requirements[req] == 1:
            total_cost -= instance.c[req]
    for req in customer_requirements_dict[customer]['requirements']:
        added_requirements[req] -= 1
    return True, total_cost, added_requirements


def heuristic_construction(customer_requirements_dict, solution, k, instance, added_requirements, total_cost, selected_customers, obj_value):
    remaining_customers = list(range(instance.m))
    while remaining_customers:
        customer = select_customer(
            remaining_customers, customer_requirements_dict, k)
        remaining_customers.remove(customer)

        if customer not in selected_customers:
            can_add_result, total_cost, added_requirements = can_add(
                customer, total_cost, added_requirements)

            if can_add_result:
                solution[customer] = 1
                obj_value += instance.w[customer]
                selected_customers.append(customer)

    return solution, total_cost, selected_customers, added_requirements, obj_value


def heuristic_destruction(customer_requirements_dict, solution, j, instance, d, selected_customers,  total_cost, obj_value, added_requirements):
    num_customers_remove = min(
        math.ceil(len(selected_customers) * d), len(selected_customers))

    for _ in range(num_customers_remove):
        customer = select_customer(
            selected_customers, customer_requirements_dict, j, True)
        selected_customers.remove(customer)
        can_remove_result, total_cost, added_requirements = can_remove(
            customer, total_cost, added_requirements)

        if can_remove_result:
            solution[customer] = 0
            obj_value -= instance.w[customer]

    return solution, total_cost, selected_customers, added_requirements, obj_value


def run_heuristic(instance, k, j, d, num_iterations=100):
    start_time = time.time()

    best_solution = 0
    best_total_cost = 0
    best_selected_customers = 0
    best_obj_value = 0

    current_solution = [0] * instance.m
    current_total_cost, selected_customers, added_requirements, obj_value = 0, [], [
        0] * instance.n, 0

    for iteration in range(num_iterations):
        current_solution, current_total_cost, selected_customers, added_requirements, obj_value = heuristic_destruction(
            customer_requirements_dict, current_solution, j, instance, d, selected_customers, current_total_cost, obj_value, added_requirements)
        current_solution, current_total_cost, selected_customers, added_requirements, obj_value = heuristic_construction(
            customer_requirements_dict, current_solution, k, instance, added_requirements, current_total_cost, selected_customers, obj_value)

        if best_obj_value < obj_value:
            best_solution = current_solution.copy()
            best_total_cost = current_total_cost
            best_selected_customers = selected_customers.copy()
            best_iteration = f"{iteration + 1}/{num_iterations}"
            best_obj_value = obj_value

    elapsed_time = time.time() - start_time
    return best_solution, best_total_cost, best_selected_customers, best_iteration, best_obj_value, elapsed_time


path = sys.argv[1]
factor = float(sys.argv[2])
instance.read(path, factor)
instance.transformation1()
k = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.5
j = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.5
d = float(sys.argv[5]) if len(sys.argv) >= 6 else 0.5

customer_requirements_dict = generate_customer_requirements_dict(instance)

solution, total_cost, selected_customers, best_iteration, best_obj_value, elapsed_time = run_heuristic(
    instance, k, j, d)

print('Solution', solution)
print('Budget', instance.b)
print('Total cost', total_cost)
print('Selected Custumers', selected_customers)
print('Best Iteration', best_iteration)
print(f'FO: {best_obj_value}')
print(f'Execution Time: {elapsed_time} seconds')
