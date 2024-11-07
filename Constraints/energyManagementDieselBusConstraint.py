from .constraint import Constraint

class EnergyManagementDieselConstraint(Constraint):
    def apply(self, model, electric_buses, diesel_buses, trips, chargers):
        def energy_management_diesel_rule(model, bus_id, trip_id):
            bus = next(d for d in diesel_buses if d.bus_id == bus_id)
            trip = next(t for t in trips if t.trip_id == trip_id)
            return model.x_d[bus_id, trip_id] * bus.remaining_range >= trip.distance * bus.consumption_rate
        model.energy_management_diesel = model.Constraint(
            [(d.bus_id, t.trip_id) for d in diesel_buses for t in trips],
            rule=energy_management_diesel_rule
        )
        print("Energy Management Diesel Bus")
