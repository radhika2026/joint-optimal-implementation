from .constraint import Constraint
class ChargingCapacityConstraint(Constraint):
    """
    Ensures that only one electric bus uses a charger at any time.
    """
    def apply(self, model, electric_buses, diesel_buses, trips, chargers):
        def charger_capacity_rule(model, charger_id, time_slot):
            return sum(model.charge[e.bus_id, time_slot] for e in electric_buses) <= 1
        model.charging_capacity = model.Constraint(
            [(charger.charger_id, t) for charger in chargers for t in range(24)],
            rule=charger_capacity_rule
        )
        print("charging capacity constraint")
