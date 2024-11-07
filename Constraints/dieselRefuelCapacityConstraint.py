from .constraint import Constraint

class DieselRefuelCapacityConstraint(Constraint):
    def apply(self, model, electric_buses, diesel_buses, trips, chargers):
        def refuel_capacity_rule(model, bus_id, time_slot):
            return model.refuel[bus_id, time_slot] <= 1  # Only one refuel session per bus per slot
        model.refuel_capacity = model.Constraint(
            [(d.bus_id, t) for d in diesel_buses for t in range(24)],
            rule=refuel_capacity_rule
        )
        print("Diesel Refuel Capacity constraint")