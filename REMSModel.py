import numpy as np
import gurobipy as gp
from gurobipy import GRB


#Given Data


# Number of people
num_people = 60

# Number of shifts
num_shifts = 60

# Binary arrays indicating whether a person is Off-Campus (1) or On-Campus (0)
#OC = np.random.randint(0, 2, num_people)

OC = [0] * num_people  # All people are initially On-Campus (0)


# Binary arrays indicating whether a person is a Non-Observer (1) or Observer (0)
num_observers = int(0.85 * num_people)  # 15% of 60 = 9 observers
O = np.zeros(num_people, dtype=int)  # Start with all as non-observers (1)
observer_indices = np.random.choice(num_people, num_observers, replace=False)
O[observer_indices] = 1  # Assign 1 (observer) to exactly 9 people

# Availability matrix (1 if available, 0 otherwise), ensuring exactly 6 available shifts per person
avail = np.zeros((num_people, num_shifts), dtype=int)
for i in range(num_people):
    available_shifts = np.random.choice(num_shifts, 6, replace=False)
    avail[i, available_shifts] = 1

# Print sample data
print("On-Campus Status (OC):", OC)
print("Observer Status (O):", O)
print("Availability Matrix:\n", avail)


#Matrix of people availability

"""
num_people = 100
num_shifts = 10

# Randomly assign each person 3 available shifts
avail = np.zeros((num_people, num_shifts), dtype=int)
np.random.seed(42)  # For reproducibility
for i in range(num_people):
    avail[i, np.random.choice(num_shifts, 6, replace=False)] = 1  # Assign 3 available shifts

# Assign some people as Duty Crew (1 = Duty Crew, 0 = not)
O = [1] * num_people

# Assign some people as Off-Campus (1 = Off-Campus, 0 = On-Campus)

OC = [0] * num_people


# Print Sample Data
print("Availability Matrix (People x Shifts):")
print(avail)
print("\nDuty Crew (O):", O)
print("\nOfficer Candidates (OC):", OC)
"""

model = gp.Model("REMS")

#Decision Variables
x = model.addVars(num_people, num_shifts, vtype=GRB.BINARY, name="x")

# buffer for no more than three people are assigned to a shift 
b = model.addVars(num_shifts, vtype=GRB.INTEGER, lb=0, name="b")

# buffer for if people are not assigned to 2 shifts 
m = model.addVars(num_people, vtype=GRB.INTEGER, lb=0, name="m")


#Objective Function

model.setObjective(sum(m[i] for i in range(num_people)) + sum(b[j] for j in range(num_shifts)), 
GRB.MINIMIZE)

#Constraints

#making sure no one is given a shift they didn't sign up for
for shift in range(num_shifts):
    for per in range(num_people):
        model.addConstr(x[per, shift] <= avail[per, shift])
    


#making sure that no more than 2 Duty Crew are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[i, shift]*O[i]  for i in range(num_people)) + b[shift] == 2)

#making sure that no more than 3 people are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[i, shift] for i in range(num_people))+ b[shift] <= 3)

#ensure that no one is assigned to more than 2 shifts
for per in range(num_people):
    model.addConstr(sum(x[per, shift] for shift in range(num_shifts)) + m[per] == 2)

#no more than 2 OC are assigned to a shift
for shift in range(num_shifts):
    model.addConstr(sum(x[per, shift]*OC[per] for per in range(num_people)) <= 2)


model.optimize()

all_vars = model.getVars()
values = model.getAttr("X", all_vars)
names = model.getAttr("VarName", all_vars)

for name, val in zip(names, values):
    print(f"{name} = {val}")

x_values = np.zeros((num_people, num_shifts))

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

# Create an empty NumPy array to store values
x_values = np.zeros((num_people, num_shifts))

# Fill the array with optimized values
for i in range(num_people):
    for j in range(num_shifts):
        x_values[i, j] = x[i, j].X  # Get the value of the decision variable

# Print the full matrix
print(x_values)