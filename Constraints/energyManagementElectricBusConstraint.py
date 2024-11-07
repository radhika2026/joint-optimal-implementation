from .constraint import Constraint

class EnergyManagementElectricConstraint(Constraint):
    """
    Ensures that electric buses have enough charge to complete assigned trips.
    """
    def apply(self, model, electric_buses, diesel_buses, trips, chargers, **kwargs):
        def energy_management_electric_rule(model, bus_id, trip_id):
            bus = next(e for e in electric_buses if e.bus_id == bus_id)
            trip = next(t for t in trips if t.trip_id == trip_id)
            return model.x_e[bus_id, trip_id] * bus.remaining_range >= trip.distance * bus.consumption_rate
        
        # Use model.Constraint, not Constraint
        model.energy_management_electric = model.Constraint(
            [(e.bus_id, t.trip_id) for e in electric_buses for t in trips],
            rule=energy_management_electric_rule
        )
        print("Energy Management Electric Bus")
