class Bus:
    """
    Base class for all types of buses (Electric and Diesel).
    Contains common attributes and methods.
    """
    def __init__(self, bus_id, capacity, consumption_rate, max_range):
        """
        Parameters:
        - bus_id: Unique identifier for the bus.
        - capacity: Passenger capacity of the bus.
        - consumption_rate: Consumption rate (fuel or charge consumption per distance unit).
        - max_range: Maximum range the bus can travel on a full charge or full tank.
        """

        self.bus_id = bus_id
        self.capacity = capacity
        self.consumption_rate = consumption_rate
        self.max_range = max_range
        self.remaining_range = max_range  # Tracks remaining fuel/charge

    def can_serve_trip(self, trip_distance):
        """
        Check if the bus has enough fuel/charge to serve a specific trip.

        Parameters:
        - trip_distance: Distance of the trip to be checked.

        Returns:
        - True if the bus can serve the trip, False otherwise.
        """
        return self.remaining_range >= trip_distance * self.consumption_rate

    def schedule_trip(self, trip_distance):
        """
        Schedule the bus for a trip, updating the remaining fuel/charge.

        Parameters:
        - trip_distance: Distance of the trip being scheduled.
        """
        if self.can_serve_trip(trip_distance):
            self.remaining_range -= trip_distance * self.consumption_rate
        else:
            raise ValueError(f"Bus {self.bus_id} does not have enough range to complete this trip.")

    def refuel_or_recharge(self):
        """
        Placeholder method for refueling or recharging.
        This will be implemented in subclasses.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")

    def __str__(self):
        """
        String representation of the Bus object.
        """
        return f"Bus {self.bus_id} - Capacity: {self.capacity}, Remaining Range: {self.remaining_range}"

