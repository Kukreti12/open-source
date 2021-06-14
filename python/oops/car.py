from vehicle import Vehicle

class Car(Vehicle):
    default_tire = "tire"

    def __init__(self, engine, tires=[], distance_traveled=0, unit="miles", **kwargs):
        super().__init__(distance_traveled=distance_traveled, unit=unit, **kwargs)
        if not tires:
            tires = [self.default_tire, self.default_tire]
        self.tires = tires
        self.engine = engine

    def drive(self, distance):
        self.distance_traveled += distance