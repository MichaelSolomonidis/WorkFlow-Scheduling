import networkx as nx #δημιουργια και διαχειριση γραφηματων

import numpy as np #για αριθμητικες πραξεις με πινακες/διανυσματα

from scipy.optimize import minimize #για βελτιστοποιηση


# Δημιουργία του γράφου επεξεργαστών

G_processors = nx.Graph()

# Προσθήκη επεξεργαστών με χαρακτηριστικά cpu και energy

G_processors.add_node(1, cpu=8, energy=50)

G_processors.add_node(2, cpu=4, energy=30)

G_processors.add_edge(1, 2, bandwidth=100)


#Δημιουργία του DAG(κατευθυνομενος ακυκλικος γραφος)τωνεργασιών

G_tasks = nx.DiGraph()

# Προσθήκη εργασιών με απαιτήσεις CPU

G_tasks.add_node(1, cpu_required=2)

G_tasks.add_node(2, cpu_required=3)

G_tasks.add_edge(1, 2, data=50) #ακμη μεταξυ 1 και 2


# Επαλήθευση της δομής των γραφημάτων

assert nx.is_directed_acyclic_graph(G_tasks), "The task graph must be a DAG"


# Συνάρτηση χρόνου εκτέλεσης

def evaluate_time_assignment(assignment):

total_time = 0

for task, processor in assignment.items():

cpu_capacity = G_processors.nodes[processor]['cpu']

task_cpu_required = G_tasks.nodes[task]['cpu_required']

total_time += task_cpu_required / cpu_capacity

return total_time


# Συνάρτηση κατανάλωσης ενέργειας

def evaluate_energy_assignment(assignment):

total_energy = 0

for task, processor in assignment.items():

energy = G_processors.nodes[processor]['energy']

total_energy += energy

return total_energy


# Συνάρτηση κόστους επικοινωνίας

def evaluate_communication_cost(assignment):

total_cost = 0

#καθε ακμη αντιπροσωπευει εξαρτηση δεδομενων μεταξυ 2 εργασιων

for u, v in G_tasks.edges():

if assignment[u] != assignment[v]:

bandwidth = G_processors[assignment[u]][assignment[v]]['bandwidth']

data = G_tasks[u][v]['data']

total_cost += data / bandwidth

return total_cost


# Συνολική συνάρτηση κόστους

def total_cost(assignment):

assignment_dict = {i+1: int(assignment[i]) for i in range(len(assignment))}

return (

evaluate_time_assignment(assignment_dict) +

evaluate_energy_assignment(assignment_dict) +

evaluate_communication_cost(assignment_dict)

)


# Εκχώρηση

initial_assignment = [1, 1] # Εκχώρηση εργασιών σε επεξεργαστές


# Περιορισμοί (διασφαλίζει ότι η χρήση CPU κάθε επεξεργαστή δεν υπερβαίνει τη διαθέσιμη CPU του επεξεργαστή αυτού.)

def constraint_cpu_capacity(assignment):

assignment_dict = {i+1: int(assignment[i]) for i in range(len(assignment))}

cpu_usage = {proc: 0 for proc in G_processors.nodes}

for task, proc in assignment_dict.items():

cpu_usage[proc] += G_tasks.nodes[task]['cpu_required']

return [G_processors.nodes[proc]['cpu'] - usage for proc, usage in cpu_usage.items()]


# Ορισμός περιορισμών ως λίστα

constraints = [{'type': 'ineq', 'fun': constraint_cpu_capacity}]


# Χρήση minimize για τη βελτιστοποίηση

result = minimize(total_cost, initial_assignment, method='COBYLA', constraints=constraints)


# Μετατροπή αποτελέσματος σε dictionary για ευκολία ανάγνωσης

optimal_assignment = {i+1: int(result.x[i]) for i in range(len(result.x))}


print(f'Optimal assignment: {optimal_assignment}')

print(f'Minimized cost: {result.fun}')
