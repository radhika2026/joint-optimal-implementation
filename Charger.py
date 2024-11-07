class Charger:
    """
    Represents a charging station for electric buses.
    """
    def __init__(self, charger_id, charging_rate):
        """
        Initialize a Charger object.

        Parameters:
        - charger_id: Unique identifier for the charger.
        - charging_rate: Rate at which the charger replenishes battery capacity per time unit.
        """
        self.charger_id = charger_id
        self.charging_rate = charging_rate
        self.schedule = {}  # Dictionary to track charging slots, e.g., {time_slot: bus_id}

    def is_available(self, time_slot):
        """
        Check if the charger is available at a given time slot.

        Parameters:
        - time_slot: Time slot to check availability.

        Returns:
        - True if the charger is available, False otherwise.
        """
        return time_slot not in self.schedule

    def schedule_charging(self, bus_id, time_slot):
        """
        Schedule a charging session for an electric bus at a specific time slot.

        Parameters:
        - bus_id: ID of the electric bus to be charged.
        - time_slot: Time slot for the charging session.

        Raises:
        - ValueError if the charger is already booked for the given time slot.
        """
        if self.is_available(time_slot):
            self.schedule[time_slot] = bus_id
        else:
            raise ValueError(f"Charger {self.charger_id} is already booked at time slot {time_slot}")

    def __str__(self):
        """
        String representation of the Charger object.
        """
        return f"Charger {self.charger_id} - Charging Rate: {self.charging_rate}, Schedule: {self.schedule}"
