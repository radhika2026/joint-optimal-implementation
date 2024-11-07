from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, Binary, minimize
import random

class RoutingProblem:
    """
    Represents the central routing optimization problem for scheduling a fleet of electric and diesel buses
    on various routes, considering recharging, refueling, and scheduling constraints.
    """
    def __init__(self, electric_buses, diesel_buses, trips, depot, constraints):
        self.electric_buses = electric_buses
        self.diesel_buses = diesel_buses
        self.trips = trips
        self.depot = depot
        self.constraints = constraints
        self.model = ConcreteModel()
        self._define_variables()
        self._apply_constraints()
        self._define_objective()

    def _define_variables(self):
        """
        Define decision variables for the optimization problem.
        """
        # Binary variables for assigning trips to electric buses
        self.model.x_e = Var(
            [(e.bus_id, trip.trip_id) for e in self.electric_buses for trip in self.trips],
            domain=Binary
        )

        # Binary variables for assigning trips to diesel buses
        self.model.x_d = Var(
            [(d.bus_id, trip.trip_id) for d in self.diesel_buses for trip in self.trips],
            domain=Binary
        )

        # Binary variables for charging and refueling
        self.model.charge = Var(
            [(e.bus_id, t) for e in self.electric_buses for t in range(24)],  # assuming 24 time slots
            domain=Binary
        )

        self.model.refuel = Var(
            [(d.bus_id, t) for d in self.diesel_buses for t in range(24)],  # assuming 24 time slots
            domain=Binary
        )

        # Binary variables for tracking if a bus is in use
        self.model.z_e = Var([e.bus_id for e in self.electric_buses], domain=Binary)
        self.model.z_d = Var([d.bus_id for d in self.diesel_buses], domain=Binary)
        print("Binary variable assigned")

    def _apply_constraints(self, initial_assignments=None):
        """
        Apply each constraint in the constraints list to the model.
        """
        for constraint in self.constraints:
            constraint.apply(self.model, electric_buses=self.electric_buses, diesel_buses=self.diesel_buses,
                             trips=self.trips, chargers=self.depot.chargers)

    def _define_objective(self):
        """
        Define the objective function to minimize total operating costs (charging and refueling costs).
        """
        fixed_cost_electric = 5  # placeholder for fixed cost of charging
        unit_cost_electric = 0.2  # placeholder for unit cost of electricity per charge unit
        fixed_cost_diesel = 3  # placeholder for fixed cost of refueling
        unit_cost_diesel = 0.1  # placeholder for unit cost of diesel per unit

        # Objective function: Minimize total operational costs
        self.model.objective = Objective(
            expr=sum(self.model.charge[e.bus_id, t] * (fixed_cost_electric + unit_cost_electric) for e in self.electric_buses for t in range(24)) +
                 sum(self.model.refuel[d.bus_id, t] * (fixed_cost_diesel + unit_cost_diesel) for d in self.diesel_buses for t in range(24)),
            sense=minimize
        )

    def _initialize_columns(self, initial_fraction=0.1):
        """
        Initialize a subset of bus-route assignments to create a restricted model.
        """
        num_assignments = int(len(self.electric_buses) * len(self.trips) * initial_fraction)
        self.initial_assignments = random.sample(
            [(e.bus_id, t.trip_id) for e in self.electric_buses for t in self.trips],
            num_assignments
        )

    def _solve_restricted_problem(self):
        """
        Solve the restricted problem using the initial subset of assignments.
        """
        # Add only the initial assignments to the model
        for assignment in self.initial_assignments:
            e_id, t_id = assignment
            self.model.x_e[e_id, t_id] = Var(domain=Binary)
        
        # Define constraints only for the restricted set
        self._apply_constraints(initial_assignments=self.initial_assignments)
        
        # Solve the restricted problem
        self.solve()

    def _add_columns(self):
        """
        Add new columns (bus-route assignments) to the model based on solution feedback.
        """
        # Find unserved trips
        unserved_trips = [t for t in self.trips if not any(self.model.x_e[e.bus_id, t.trip_id].value == 1 for e in self.electric_buses)]
        
        # Randomly assign an electric bus to each unserved trip to create a new assignment
        for trip in unserved_trips:
            bus = random.choice(self.electric_buses)
            new_assignment = (bus.bus_id, trip.trip_id)
            
            # Only add if it’s not already in the model
            if new_assignment not in self.initial_assignments:
                self.initial_assignments.append(new_assignment)
                self.model.x_e[bus.bus_id, trip.trip_id] = Var(domain=Binary)

    def solve_with_column_generation(self, tolerance=1e-4, max_iterations=10):
        """
        Solve the routing problem using column generation.
        """
        self._initialize_columns()
        
        last_objective_value = float('inf')
        for iteration in range(max_iterations):
            print(f"Iteration {iteration + 1}")
            
            # Solve the restricted problem with current columns
            self._solve_restricted_problem()
            
            # Check for improvement
            current_objective_value = self.model.objective.expr()
            improvement = last_objective_value - current_objective_value
            print(f"Objective value: {current_objective_value}, Improvement: {improvement}")
            
            if improvement < tolerance:
                print("Convergence achieved.")
                break
            
            # Update last objective and add new columns
            last_objective_value = current_objective_value
            self._add_columns()

    def solve(self):
        """
        Solve the optimization problem.
        """
        solver = SolverFactory('glpk')  # Placeholder solver; replace with 'gurobi' or other suitable solver
        solution = solver.solve(self.model, tee=True)
        return solution

    def display_solution(self):
        """
        Display the solution in a readable format.
        """
        for e in self.electric_buses:
            for trip in self.trips:
                if self.model.x_e[e.bus_id, trip.trip_id].value == 1:
                    print(f"Electric Bus {e.bus_id} assigned to Trip {trip.trip_id}")

        for d in self.diesel_buses:
            for trip in self.trips:
                if self.model.x_d[d.bus_id, trip.trip_id].value == 1:
                    print(f"Diesel Bus {d.bus_id} assigned to Trip {trip.trip_id}")
