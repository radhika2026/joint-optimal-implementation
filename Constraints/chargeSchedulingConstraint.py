from .constraint import Constraint

class ChargerSchedulingConstraint(Constraint):
    def apply(self, model, electric_buses, diesel_buses, trips, chargers, **kwargs):
        def charger_scheduling_rule(model, bus_id, trip_id, next_trip_id):
            bus = next(e for e in electric_buses if e.bus_id == bus_id)
            trip = next(t for t in trips if t.trip_id == trip_id)
            next_trip = next(t for t in trips if t.trip_id == next_trip_id)
            
            # Convert to integer to make it compatible with Pyomo
            charging_needed = int((trip.distance + next_trip.distance) * bus.consumption_rate > bus.remaining_range)
            
            return model.charge[bus_id, trip.end_time] >= charging_needed * model.x_e[bus_id, next_trip_id]
        
        # Use a dictionary to store the constraints before adding them to the model
        charger_constraints = {}
        
        # Dynamically create and apply constraints only for valid trip pairs
        for e in electric_buses:
            for t in trips:
                for n in trips:
                    if t.trip_id != n.trip_id and t.end_time <= n.start_time:
                        constraint_name = f"charger_scheduling_{e.bus_id}_{t.trip_id}_{n.trip_id}"
                        charger_constraints[(e.bus_id, t.trip_id, n.trip_id)] = charger_scheduling_rule(
                            model, e.bus_id, t.trip_id, n.trip_id
                        )
        
        # Add all constraints as a single indexed constraint block to the model
        model.charger_scheduling = Constraint(
            charger_constraints.keys(),
            rule=lambda model, bus_id, trip_id, next_trip_id: charger_constraints[(bus_id, trip_id, next_trip_id)]
        )

        print("Charge scheduling Constraint")
