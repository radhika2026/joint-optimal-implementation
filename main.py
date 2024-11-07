import random
from Bus.ElectricBus import ElectricBus
from Bus.FuelBus import FuelBus
from Trip import Trip
from Charger import Charger
from Depot import Depot
from Constraints.chargeSchedulingConstraint import *
from Constraints.chargingCapacityConstraint import *
from Constraints.depotConstraint import *
from Constraints.dieselRefuelCapacityConstraint import *
from Constraints.energyManagementDieselBusConstraint import *
from Constraints.energyManagementElectricBusConstraint import *
from Constraints.fleetSizeConstraints import *
from Constraints.tripCompletionConstraints import *
from RoutingProblem import RoutingProblem
# Constants
NUM_ELECTRIC_BUSES = 500
NUM_DIESEL_BUSES = 1500
NUM_TRIPS = 5000
NUM_CHARGERS = 100
TIME_SLOTS = 24  # Assuming 24 hours for simplicity

# Generate Electric Buses
electric_buses = [
    ElectricBus(
        bus_id=f"E{i+1}",
        capacity=random.randint(30, 60),
        consumption_rate=round(random.uniform(0.15, 0.3), 2),
        battery_capacity=random.randint(100, 200),
        charging_rate=random.randint(10, 20)
    )
    for i in range(NUM_ELECTRIC_BUSES)
]
print("Generated Electric Bus Objects.")

# Generate Diesel Buses
fuel_buses = [
    FuelBus(
        bus_id=f"D{i+1}",
        capacity=random.randint(40, 70),
        consumption_rate=round(random.uniform(0.08, 0.15), 2),
        fuel_capacity=random.randint(200, 300)
    )
    for i in range(NUM_DIESEL_BUSES)
]
print("Generated Fuel Bus Objects.")

# Generate Trips
trips = [
    Trip(
        trip_id=f"T{i+1}",
        start_time=random.randint(6, 22),  # Random start hour between 6 AM and 10 PM
        end_time=random.randint(6, 22),  # Random end hour between 6 AM and 10 PM, adjusted later to ensure end_time > start_time
        distance=random.randint(10, 50),  # Random trip distance between 10 and 50 miles
        demand=random.randint(20, 60),  # Random demand between 20 and 60 passengers
        origin=f"Location{random.randint(1, 10)}",  # Random location ID for origin
        destination=f"Location{random.randint(1, 10)}"  # Random location ID for destination
    )
    for i in range(NUM_TRIPS)
]

# Adjust trips to ensure end_time > start_time
for trip in trips:
    if trip.end_time <= trip.start_time:
        trip.end_time = trip.start_time + random.randint(1, 2)

print("Generated Trips.")

# Generate Chargers
chargers = [
    Charger(charger_id=f"C{i+1}", charging_rate=random.randint(10, 20))
    for i in range(NUM_CHARGERS)
]

print("Generated Chargers.")

# Initialize Depot with buses and chargers
depot = Depot(location="Depot", electric_buses=electric_buses, diesel_buses=fuel_buses, chargers=chargers)
print("Generated Depot")

constraints = [
    TripCompletionConstraint(),
    FleetSizeConstraint(),
    EnergyManagementElectricConstraint(),
    ChargingCapacityConstraint(),
    DieselRefuelCapacityConstraint(),
    EnergyManagementDieselConstraint(),
    ChargerSchedulingConstraint(),
    DepotReturnConstraint()
]

# Initialize the RoutingProblem with buses, trips, depot, and constraints
routing_problem = RoutingProblem(electric_buses, fuel_buses, trips, depot, constraints)

# Solve the optimization problem
solution = routing_problem.solve()
