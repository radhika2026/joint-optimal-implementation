import numpy as np
import random

# Input Data
routes = ["R1", "R2", "R3", "R4"]
buses = ["BEB1", "BEB2", "FCEB1", "FCEB2"]
energy_capacity = {"BEB1": 100, "BEB2": 120, "FCEB1": 200, "FCEB2": 220}  # Energy capacities
energy_consumption = {"R1": 40, "R2": 50, "R3": 60, "R4": 80}  # Energy required for each route
charging_capacity = 2  # Number of chargers at depots
opportunity_charging_capacity = 2
opportunity_charging_stations = ["OC1", "OC2"]
refueling_stations = ["RS1", "RS2"]
refueling_station_capacity = {"RS1": 1, "RS2": 1}

# Mapping of routes to opportunity chargers and refueling stations
route_to_opportunity_chargers = {
    "R1": ["OC1"],
    "R2": ["OC1", "OC2"],
    "R3": ["OC2"],
    "R4": ["OC1", "OC2"]
}
route_to_refueling_stations = {
    "R1": ["RS1"],
    "R2": ["RS1", "RS2"],
    "R3": ["RS2"],
    "R4": ["RS1", "RS2"]
}

def initialize_state():
    """Generate a random initial state."""
    state = {}
    for route in routes:
        state[route] = random.choice(buses)
    return state

def calculate_cost(state, return_separate_costs=False):
    """Calculate the cost of the given state."""
    operational_cost = 0
    penalties = 0

    # Operational cost for each route
    for route, bus in state.items():
        if energy_consumption[route] > energy_capacity[bus]:
            penalties += 5000  # Large penalty for infeasible assignments
        else:
            operational_cost += energy_consumption[route] * 10  # Example cost multiplier

    # Charger utilization constraint
    charger_usage = {bus: 0 for bus in buses}
    for route, bus in state.items():
        charger_usage[bus] += 1

    if max(charger_usage.values()) > charging_capacity:
        penalties += 1000  # Penalty for overloading chargers

    # Energy balancing constraint
    avg_energy = sum(energy_consumption[route] for route in routes) / len(buses)
    for bus in buses:
        bus_energy_usage = sum(
            energy_consumption[route] for route, assigned_bus in state.items() if assigned_bus == bus
        )
        penalties += abs(bus_energy_usage - avg_energy) * 10  # Weight for energy imbalance

    # Opportunity charging constraint
    opportunity_charger_usage = {station: 0 for station in opportunity_charging_stations}
    for route, bus in state.items():
        if bus.startswith("BEB"):  # Assuming BEBs use opportunity chargers
            available_stations = route_to_opportunity_chargers.get(route, [])
            if not available_stations:
                penalties += 1000  # No charger available on the route
            else:
                assigned_station = random.choice(available_stations)
                opportunity_charger_usage[assigned_station] += 1
    if any(usage > opportunity_charging_capacity for usage in opportunity_charger_usage.values()):
        penalties += 1000

    # Refueling constraint
    refueling_usage = {station: 0 for station in refueling_stations}
    for route, bus in state.items():
        if bus.startswith("FCEB"):  # Assuming FCEBs use refueling stations
            available_stations = route_to_refueling_stations.get(route, [])
            if not available_stations:
                penalties += 1000  # No refueling station available on the route
            else:
                assigned_station = random.choice(available_stations)
                refueling_usage[assigned_station] += 1
    if any(usage > refueling_station_capacity[station] for station, usage in refueling_usage.items()):
        penalties += 1000

    if return_separate_costs:
        return operational_cost, penalties
    return operational_cost + penalties

def validate_and_recalculate(state):
    """Validate the final state against all constraints and recalculate the cost."""
    operational_cost, penalties = calculate_cost(state, return_separate_costs=True)
    violations = []

    # Validate each route
    for route, bus in state.items():
        if energy_consumption[route] > energy_capacity[bus]:
            violations.append(f"Route {route} exceeds {bus}'s capacity.")

    # Opportunity charging and refueling validation
    opp_charging_usage = {station: 0 for station in opportunity_charging_stations}
    refueling_usage = {station: 0 for station in refueling_stations}

    for route, bus in state.items():
        if bus.startswith("BEB"):
            chargers = route_to_opportunity_chargers.get(route, [])
            if not chargers:
                violations.append(f"Route {route} has no chargers available for {bus}.")
            else:
                for charger in chargers:
                    opp_charging_usage[charger] += 1
        elif bus.startswith("FCEB"):
            stations = route_to_refueling_stations.get(route, [])
            if not stations:
                violations.append(f"Route {route} has no refueling station available for {bus}.")
            else:
                for station in stations:
                    refueling_usage[station] += 1

    # Check charger and refueling station usage
    if any(usage > opportunity_charging_capacity for usage in opp_charging_usage.values()):
        violations.append("Opportunity chargers are overloaded.")
    if any(usage > refueling_station_capacity[station] for station, usage in refueling_usage.items()):
        violations.append("Refueling stations are overloaded.")

    return operational_cost, penalties, violations

def generate_neighbor(state):
    """Generate a neighboring state by swapping assignments."""
    neighbor = state.copy()
    route_to_change = random.choice(routes)
    current_bus = neighbor[route_to_change]
    new_bus = random.choice([bus for bus in buses if bus != current_bus])

    # Ensure new assignment is feasible
    if energy_consumption[route_to_change] <= energy_capacity[new_bus]:
        neighbor[route_to_change] = new_bus
    return neighbor

def simulated_annealing(initial_state, initial_temp, cooling_rate, max_iterations):
    """Simulated Annealing Algorithm."""
    current_state = initial_state
    current_cost = calculate_cost(current_state)
    best_state = current_state
    best_cost = current_cost

    temperature = initial_temp

    for iteration in range(max_iterations):
        # print(f"Iteration {iteration + 1}: Current State = {current_state}, Current Cost = {current_cost}, Temperature = {temperature}")
        neighbor = generate_neighbor(current_state)
        neighbor_cost = calculate_cost(neighbor)

        # Calculate acceptance probability
        delta_cost = neighbor_cost - current_cost
        if delta_cost < 0 or np.exp(-delta_cost / temperature) > random.random():
            current_state = neighbor
            current_cost = neighbor_cost

            # Update the best state if improved
            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost
                print(f"--> New Best State Found: {best_state} with Cost: {best_cost}")

        # Cool the temperature
        temperature *= cooling_rate

        # Stopping condition
        if temperature < 1e-3:
            break

    return best_state, best_cost

# Parameters
initial_state = initialize_state()
initial_temp = 1000
cooling_rate = 0.95
max_iterations = 1000

# Run Simulated Annealing
best_state, best_cost = simulated_annealing(initial_state, initial_temp, cooling_rate, max_iterations)

print("Best State:", best_state)
print("Best Cost:", best_cost)

# Validate final solution
final_operational_cost, penalties, violations = validate_and_recalculate(best_state)
print("Final Operational Cost:", final_operational_cost)
print("Penalties:", penalties)
if violations:
    print("Violations:", violations)
else:
    print("No violations found. Solution is valid.")
