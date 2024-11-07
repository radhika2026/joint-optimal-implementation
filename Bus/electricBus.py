from .Bus import Bus
class ElectricBus(Bus):
    """
    Represents an electric bus, subclass of Bus.
    """
    def __init__(self, bus_id, capacity, consumption_rate, battery_capacity, charging_rate):
        """
        Initialize an ElectricBus object.

        Parameters:
        - battery_capacity: Maximum battery capacity (full charge range).
        - charging_rate: Rate at which the bus can be charged.
        """
        super().__init__(bus_id, capacity, consumption_rate, battery_capacity)
        self.charging_rate = charging_rate
        self.battery_capacity = battery_capacity

    def recharge(self):
        """
        Recharge the electric bus to its maximum battery capacity.
        """
        self.remaining_range = self.battery_capacity

    def __str__(self):
        """
        String representation of the ElectricBus object.
        """
        return f"ElectricBus {self.bus_id} - Capacity: {self.capacity}, Remaining Battery: {self.remaining_range}"
