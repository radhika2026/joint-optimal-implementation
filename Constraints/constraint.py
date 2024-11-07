class Constraint:
    """
    Base class for defining constraints in the routing problem.
    Each specific constraint will inherit from this class.
    """
    def apply(self, model, **kwargs):
        """
        Apply the constraint to the Pyomo model.
        This method should be implemented by subclasses.

        Parameters:
        - model: The Pyomo model to which the constraint is added.
        """
        raise NotImplementedError("Subclasses should implement this method.")
