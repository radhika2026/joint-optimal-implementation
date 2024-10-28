import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Number of trips
N = 3 

# Trips including dummy start (0) and end (N+1)
trip_indices = [0] + list(range(1, N+1)) + [N+1]  # [0, 1, 2, 3, 4]

# Start and end times for trips (including dummy nodes)
a_dict = {
    0: 0,    # Dummy start node
    1: 2,    # Trip 1 starts at time 2
    2: 5,    # Trip 2 starts at time 5
    3: 8,    # Trip 3 starts at time 8
    4: 12    # Dummy end node (arbitrary value beyond last trip)
}

b_dict = {
    0: 0,    # Dummy start node
    1: 4,    # Trip 1 ends at time 4
    2: 7,    # Trip 2 ends at time 7
    3: 10,   # Trip 3 ends at time 10
    4: 12    # Dummy end node (arbitrary value)
}

# Distance of each trip (including dummy nodes)
d_dict = {
    0: 0,    # Dummy start node
    1: 10,   # Distance of trip 1
    2: 15,   # Distance of trip 2
    3: 20,   # Distance of trip 3
    4: 0     # Dummy end node (N+1)
}

# Distances from depot to start of trips (dds) and from end of trips to depot (ded)
dds_dict = {
    0: 0,
    1: 5,    # Depot to start of trip 1
    2: 5,    # Depot to start of trip 2
    3: 5,    # Depot to start of trip 3
    4: 0     # Not used
}

ded_dict = {
    0: 0,
    1: 5,    # End of trip 1 to depot
    2: 5,    # End of trip 2 to depot
    3: 5,    # End of trip 3 to depot
    4: 0     # Not used
}

# Deadhead distances between trips (assuming 2 units between any two trips)
d_ij_dict = {}
for i in trip_indices:
    for j in trip_indices:
        if i == 0:
            d_ij_dict[(i, j)] = dds_dict[j]  # From depot to start of trip j
        elif j == N+1:
            d_ij_dict[(i, j)] = ded_dict[i]  # From end of trip i to depot
        elif i != j:
            d_ij_dict[(i, j)] = 2            # Distance between trips
        else:
            d_ij_dict[(i, j)] = 0            # Same trip

# Number of buses
num_electric_buses = 2
num_diesel_buses = 2

# Number of chargers
num_chargers = 1

# Number of time slots
time_slots = list(range(1, 13))  # Time slots from 1 to 12

# Cost parameters
alpha_0_value = 5    # Fixed cost per charging session
alpha_1_value = 0.1  # Unit electricity cost per kWh
alpha_2_value = 3    # Fixed cost per refueling session
alpha_3_value = 0.05 # Unit diesel cost per liter

# Energy parameters
r1_value = 50        # Charging rate (kWh per time unit)
u1_value = 1         # Charging time interval (1 time unit)
r2_value = 100       # Refueling rate (liters per time unit)
u2_value = 1         # Refueling time interval (1 time unit)

# Capacities
Q_value = 300        # Battery capacity (kWh)
C_value = 500        # Diesel capacity (liters)
Q_min_value = 50     # Minimum remaining charge (kWh)
C_min_value = 100    # Minimum remaining diesel (liters)

# Energy consumption rates
c1_value = 2         # Energy consumption rate (kWh per km) for electric buses
c2_value = 0.5       # Energy consumption rate (liters per km) for diesel buses

def feasible(i, j):
    if i == N+1 or j == 0:
        return False
    if i == 0 and j != N+1:
        return True  # From dummy start node to any trip except dummy end node
    if i != N+1 and j == N+1:
        return True  # From any trip to dummy end node
    if i != 0 and j != N+1:
        travel_time = 1  # Assume 1 time unit travel time between trips
        if i in b_dict and j in a_dict:
            if b_dict[i] + travel_time <= a_dict[j]:
                return True
    return False

big_M_value = 1000

# Sets
I0_N1 = trip_indices

P = []
P_star = []

for i in I0_N1:
    for j in I0_N1:
        if feasible(i, j):
            P.append((i, j))
            if i != N+1 and j != 0:
                P_star.append((i, j))

# Create a model instance
model = pyo.ConcreteModel()

# Sets
model.I = pyo.Set(initialize=trip_indices)
model.E = pyo.Set(initialize=range(1, num_electric_buses + 1))
model.D = pyo.Set(initialize=range(1, num_diesel_buses + 1))
model.K = pyo.Set(initialize=range(1, num_chargers + 1))
model.T = pyo.Set(initialize=time_slots)
model.P = pyo.Set(dimen=2, initialize=P)
model.P_star = pyo.Set(dimen=2, initialize=P_star)

# Parameters
model.alpha_0 = pyo.Param(initialize=alpha_0_value)
model.alpha_1 = pyo.Param(initialize=alpha_1_value)
model.alpha_2 = pyo.Param(initialize=alpha_2_value)
model.alpha_3 = pyo.Param(initialize=alpha_3_value)
model.r1 = pyo.Param(initialize=r1_value)
model.u1 = pyo.Param(initialize=u1_value)
model.r2 = pyo.Param(initialize=r2_value)
model.u2 = pyo.Param(initialize=u2_value)
model.Q = pyo.Param(initialize=Q_value)
model.C = pyo.Param(initialize=C_value)
model.Q_min = pyo.Param(initialize=Q_min_value)
model.C_min = pyo.Param(initialize=C_min_value)
model.c1 = pyo.Param(initialize=c1_value)
model.c2 = pyo.Param(initialize=c2_value)
model.d = pyo.Param(model.I, initialize=d_dict)
model.a = pyo.Param(model.I, initialize=a_dict)
model.b = pyo.Param(model.I, initialize=b_dict)
model.d_ij = pyo.Param(model.I, model.I, initialize=d_ij_dict)

# Variables
model.z_e = pyo.Var(model.E, domain=pyo.Binary)
model.z_d = pyo.Var(model.D, domain=pyo.Binary)
model.F_ie = pyo.Var(model.I, model.E, domain=pyo.Binary)
model.F_id = pyo.Var(model.I, model.D, domain=pyo.Binary)
model.x_ije = pyo.Var(model.P, model.E, domain=pyo.Binary)
model.x_ijd = pyo.Var(model.P, model.D, domain=pyo.Binary)
model.Q_ie = pyo.Var(model.I, model.E, bounds=(0, model.Q))
model.Q_id = pyo.Var(model.I, model.D, bounds=(0, model.C))

# Objective Function
def objective_rule(model):
    charging_costs = sum(
        (model.alpha_0 + model.alpha_1 * model.r1 * model.u1) * model.F_ie[i, e]
        for i in model.I for e in model.E
    )
    refueling_costs = sum(
        (model.alpha_2 + model.alpha_3 * model.r2 * model.u2) * model.F_id[i, d]
        for i in model.I for d in model.D
    )
    # Operational costs for electric buses
    operational_costs_e = sum(
        model.alpha_1 * model.c1 * (model.d_ij[i, j] + model.d[j]) * model.x_ije[i, j, e]
        for (i, j) in model.P for e in model.E
    )
    # Operational costs for diesel buses
    operational_costs_d = sum(
    model.alpha_3 * model.c2 * (model.d_ij[i, j] + model.d[j]) * model.x_ijd[i, j, d]
    for (i, j) in model.P for d in model.D
)
    return charging_costs + refueling_costs + operational_costs_e + operational_costs_d
model.obj = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

# Constraints

def initial_charge_e_rule(model, e):
    return model.Q_ie[0, e] == model.Q
model.initial_charge_e = pyo.Constraint(model.E, rule=initial_charge_e_rule)

def initial_diesel_d_rule(model, d):
    return model.Q_id[0, d] == model.C
model.initial_diesel_d = pyo.Constraint(model.D, rule=initial_diesel_d_rule)

def trip_served_rule(model, i):
    if i == 0 or i == N+1:
        return pyo.Constraint.Skip
    return sum(model.x_ije[j, i, e] for (j, i2) in model.P if i2 == i for e in model.E) + \
           sum(model.x_ijd[j, i, d] for (j, i2) in model.P if i2 == i for d in model.D) == 1
model.trip_served = pyo.Constraint(model.I, rule=trip_served_rule)

# Limit on Number of Buses
model.electric_bus_limit = pyo.Constraint(expr=sum(model.z_e[e] for e in model.E) <= num_electric_buses)
model.diesel_bus_limit = pyo.Constraint(expr=sum(model.z_d[d] for d in model.D) <= num_diesel_buses)

def vehicle_scheduling_e_rule(model, e):
    return sum(model.x_ije[i, j, e] for (i, j) in model.P) <= model.z_e[e] * big_M_value
model.vehicle_scheduling_e = pyo.Constraint(model.E, rule=vehicle_scheduling_e_rule)

def vehicle_scheduling_d_rule(model, d):
    return sum(model.x_ijd[i, j, d] for (i, j) in model.P) <= model.z_d[d] * big_M_value
model.vehicle_scheduling_d = pyo.Constraint(model.D, rule=vehicle_scheduling_d_rule)

def charging_after_trip_e_rule(model, i, e):
    return model.F_ie[i, e] <= sum(model.x_ije[i, j, e] for (i2, j) in model.P if i2 == i)
model.charging_after_trip_e = pyo.Constraint(model.I, model.E, rule=charging_after_trip_e_rule)

def refueling_after_trip_d_rule(model, i, d):
    return model.F_id[i, d] <= sum(model.x_ijd[i, j, d] for (i2, j) in model.P if i2 == i)
model.refueling_after_trip_d = pyo.Constraint(model.I, model.D, rule=refueling_after_trip_d_rule)

def remaining_charge_rule(model, i, j, e):
    if (i, j) in model.P_star:
        return model.x_ije[i, j, e] * model.Q_min <= model.Q_ie[j, e]
    else:
        return pyo.Constraint.Skip
model.remaining_charge_min = pyo.Constraint(model.P_star, model.E, rule=remaining_charge_rule)

def remaining_diesel_rule(model, i, j, d):
    if (i, j) in model.P_star:
        energy_gain = (model.r2 * model.u2) * model.F_id[i, d]
        energy_consumption = model.c2 * (model.d_ij[i, j] + model.d[j]) * model.x_ijd[i, j, d]
        return model.Q_id[j, d] <= model.Q_id[i, d] + energy_gain - energy_consumption
    else:
        return pyo.Constraint.Skip

model.remaining_diesel_min = pyo.Constraint(model.P_star, model.D, rule=remaining_diesel_rule)

def remaining_charge_max_rule(model, i, j, e):
    if (i, j) in model.P_star:
        energy_gain = (model.r1 * model.u1) * model.F_ie[i, e]
        energy_consumption = model.c1 * (model.d_ij[i, j] + model.d[j]) * model.x_ije[i, j, e]
        return model.Q_ie[j, e] <= model.Q_ie[i, e] + energy_gain - energy_consumption
    else:
        return pyo.Constraint.Skip
model.remaining_charge_max = pyo.Constraint(model.P_star, model.E, rule=remaining_charge_max_rule)

def remaining_diesel_max_rule(model, i, j, d):
    if (i, j) in model.P_star:
        energy_gain = (model.r2 * model.u2) * model.F_id[i, d]
        energy_consumption = model.c2 * (model.d_ij[i, j] + model.d[j]) * model.x_ijd[i, j, d]
        return model.Q_id[j, d] <= model.Q_id[i, d] + energy_gain - energy_consumption
    else:
        return pyo.Constraint.Skip
model.remaining_diesel_max = pyo.Constraint(model.P_star, model.D, rule=remaining_diesel_max_rule)

def capacity_constraint_e_rule(model, i, e):
    return model.Q_ie[i, e] <= model.Q
model.capacity_constraint_e = pyo.Constraint(model.I, model.E, rule=capacity_constraint_e_rule)

def capacity_constraint_d_rule(model, i, d):
    return model.Q_id[i, d] <= model.C
model.capacity_constraint_d = pyo.Constraint(model.I, model.D, rule=capacity_constraint_d_rule)

# Solver
solver = SolverFactory('glpk')

# Solve the model
result = solver.solve(model, tee=True)

# Check solver status
if (result.solver.status == pyo.SolverStatus.ok) and (result.solver.termination_condition == pyo.TerminationCondition.optimal):
    print('Solver found an optimal solution.')
elif result.solver.termination_condition == pyo.TerminationCondition.infeasible:
    print('Solver found the problem infeasible.')
else:
    print('Solver status:', result.solver.status)
    print('Termination condition:', result.solver.termination_condition)

# Retrieve Results
print('Total Cost:', pyo.value(model.obj))

# Decision variables
for e in model.E:
    if pyo.value(model.z_e[e]) > 0.5:
        print(f'Electric Bus {e} is scheduled.')
        route = []
        current_trip = 0  # Start from dummy start node
        while True:
            next_trips = [j for (i, j) in model.P if i == current_trip and pyo.value(model.x_ije[i, j, e]) > 0.5]
            if not next_trips:
                break
            next_trip = next_trips[0]
            if next_trip == N+1:
                break
            route.append(next_trip)
            current_trip = next_trip
        print(f'  Route: {route}')
        # Check if bus charges after trips
        for i in route:
            if pyo.value(model.F_ie[i, e]) > 0.5:
                print(f'  Electric Bus {e} charges after trip {i}')

for d in model.D:
    if pyo.value(model.z_d[d]) > 0.5:
        print(f'Diesel Bus {d} is scheduled.')
        route = []
        current_trip = 0  # Start from dummy start node
        while True:
            next_trips = [j for (i, j) in model.P if i == current_trip and pyo.value(model.x_ijd[i, j, d]) > 0.5]
            if not next_trips:
                break
            next_trip = next_trips[0]
            if next_trip == N+1:
                break
            route.append(next_trip)
            current_trip = next_trip
        print(f'  Route: {route}')
        # Check if bus refuels after trips
        for i in route:
            if pyo.value(model.F_id[i, d]) > 0.5:
                print(f'  Diesel Bus {d} refuels after trip {i}')