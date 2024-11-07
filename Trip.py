class Trip:
    """
    Represents a specific trip in the schedule.
    """
    def __init__(self, trip_id, start_time, end_time, distance, demand, origin, destination):
        """
        Initialize a Trip object.

        Parameters:
        - trip_id: Unique identifier for the trip.
        - start_time: Start time of the trip.
        - end_time: End time of the trip.
        - distance: Distance of the trip.
        - demand: Passenger demand for the trip.
        - origin: Starting location of the trip.
        - destination: Ending location of the trip.
        """
        self.trip_id = trip_id
        self.start_time = start_time
        self.end_time = end_time
        self.distance = distance
        self.demand = demand
        self.origin = origin
        self.destination = destination

    def duration(self):
        """
        Calculate and return the duration of the trip.

        Returns:
        - Duration of the trip as the difference between end time and start time.
        """
        return self.end_time - self.start_time

    def distance_from_other_trip(self, other_trip, default_distance=10):
        """
        Calculate the hypothetical distance from the destination of this trip to the origin of another trip.

        Parameters:
        - other_trip: Another Trip object to calculate the distance to.
        - default_distance: Placeholder distance to use for demonstration (default is 10).

        Returns:
        - Placeholder distance between this trip's destination and the other trip's origin.
        """
        # Here we return a default distance for simplicity.
        # In real-world applications, calculate this based on geographic coordinates.
        return default_distance

    def __str__(self):
        """
        String representation of the Trip object.
        """
        return (f"Trip {self.trip_id} - From {self.origin} to {self.destination}, "
                f"Start: {self.start_time}, End: {self.end_time}, Distance: {self.distance}, Demand: {self.demand}")

