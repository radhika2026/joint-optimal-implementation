from .constraint import Constraint

class DepotReturnConstraint(Constraint):
    def apply(self, model, electric_buses, diesel_buses, trips, chargers):
        final_trip_id = max(trip.trip_id for trip in trips)  # assuming trips are sequentially ordered
        
        def depot_return_rule_electric(model, bus_id):
            return model.x_e[bus_id, final_trip_id] >= 1  # Ensure last trip returns to depot
        model.depot_return_electric = Constraint(
            [e.bus_id for e in electric_buses],
            rule=depot_return_rule_electric
        )

        def depot_return_rule_diesel(model, bus_id):
            return model.x_d[bus_id, final_trip_id] >= 1  # Ensure last trip returns to depot
        model.depot_return_diesel = Constraint(
            [d.bus_id for d in diesel_buses],
            rule=depot_return_rule_diesel
        )
        print("Depot Return Constraint")
