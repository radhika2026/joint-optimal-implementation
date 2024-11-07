from .Bus import Bus
class FuelBus(Bus):
    """
    Represents a diesel bus, subclass of Bus.
    """
    def __init__(self, bus_id, capacity, consumption_rate, fuel_capacity):
        """
        Initialize a DieselBus object.

        Parameters:
        - fuel_capacity: Maximum fuel capacity (full tank range).
        """
        super().__init__(bus_id, capacity, consumption_rate, fuel_capacity)
        self.fuel_capacity = fuel_capacity

    def refuel(self):
        """
        Refuel the diesel bus to its maximum fuel capacity.
        """
        self.remaining_range = self.fuel_capacity

    def __str__(self):
        """
        String representation of the DieselBus object.
        """
        return f"DieselBus {self.bus_id} - Capacity: {self.capacity}, Remaining Fuel: {self.remaining_range}"

