class Vehicle:
    """
    Vehicle models a device that can be used to travel.
    """
    def __init__(self, distance_traveled=0, unit='miles'):
        self.distance_traveled = distance_traveled
        self.unit = unit

    def description(self):
        return f"A {self.__class__.__name__} that has traveled {self.distance_traveled} {self.unit}"