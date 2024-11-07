from Bus.ElectricBus import ElectricBus
from Bus.FuelBus import FuelBus
class Depot:
    """
    Represents the depot where buses start, end, recharge, and refuel.
    """
    def __init__(self, location, electric_buses, diesel_buses, chargers):
        """
        Initialize a Depot object.

        Parameters:
        - location: Location of the depot.
        - electric_buses: List of electric Bus objects.
        - diesel_buses: List of diesel Bus objects.
        - chargers: List of Charger objects at the depot.
        """
        self.location = location
        self.electric_buses = electric_buses  # List of ElectricBus instances
        self.diesel_buses = diesel_buses      # List of DieselBus instances
        self.chargers = chargers              # List of Charger instances

    def assign_bus(self, bus, trip):
        """
        Assign a bus to a trip and update its remaining range accordingly.

        Parameters:
        - bus: Bus object to be assigned to the trip.
        - trip: Trip object representing the trip to be assigned.
        """
        bus.schedule_trip(trip.distance)

    def refuel_or_recharge(self, bus):
        """
        Refuel or recharge a bus based on its type.

        Parameters:
        - bus: Bus object to be refueled or recharged.
        """
        if isinstance(bus, ElectricBus):
            bus.recharge()
        elif isinstance(bus, FuelBus):
            bus.refuel()
        else:
            raise ValueError("Unknown bus type")

    def schedule_charging(self, bus, time_slot):
        """
        Schedule charging for an electric bus at the depot's available chargers.

        Parameters:
        - bus: ElectricBus object that needs to be charged.
        - time_slot: Time slot for the charging session.

        Raises:
        - ValueError if no charger is available at the given time slot.
        """
        for charger in self.chargers:
            if charger.is_available(time_slot):
                charger.schedule_charging(bus.bus_id, time_slot)
                return
        raise ValueError("No available chargers at the specified time slot")

    def __str__(self):
        """
        String representation of the Depot object.
        """
        return (f"Depot at {self.location} - Electric Buses: {len(self.electric_buses)}, "
                f"Diesel Buses: {len(self.diesel_buses)}, Chargers: {len(self.chargers)}")
