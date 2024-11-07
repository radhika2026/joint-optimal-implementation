from .constraint import Constraint

class TripCompletionConstraint(Constraint):
    """
    Ensures that each trip is served by exactly one bus (either electric or diesel).
    """
    def apply(self, model, electric_buses, diesel_buses, trips, chargers, **kwargs):
        def trip_completion_rule(model, trip_id):
            return (
                sum(model.x_e[e.bus_id, trip_id] for e in electric_buses if (e.bus_id, trip_id) in model.x_e) +
                sum(model.x_d[d.bus_id, trip_id] for d in diesel_buses if (d.bus_id, trip_id) in model.x_d)
            ) == 1

        # Use model.Constraint, not Constraint
        model.trip_completion_constraint = model.Constraint(
            [trip.trip_id for trip in trips], rule=trip_completion_rule
        )

        print("each trip is served by exactly one bus ")
