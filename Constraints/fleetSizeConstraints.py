from .constraint import Constraint

class FleetSizeConstraint(Constraint):
    """
    Limits the number of electric and diesel buses used to the available fleet.
    """
    def apply(self, model, electric_buses, diesel_buses, trips, chargers, **kwargs):
        model.fleet_size_electric = model.Constraint(
            expr=sum(model.z_e[e.bus_id] for e in electric_buses) <= len(electric_buses)
        )
        model.fleet_size_diesel = model.Constraint(
            expr=sum(model.z_d[d.bus_id] for d in diesel_buses) <= len(diesel_buses)
        )
        print("Fleet size")