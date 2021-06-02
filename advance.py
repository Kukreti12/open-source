class Vehicle:
    """
    Vehicle models a vehicle w/ tires and an engine
    """
    default_tire = 'tire'

    def __init__(self, engine, tires):
        self.engine = engine
        self.tires = tires

    @classmethod
    def bicycle(cls, tires=None):
        if not tires:
            tires = [cls.default_tire, cls.default_tire]
        return cls(None, tires)

    def description(self):
        print(f"A vehicle with an {self.engine} engine, and {self.tires} tires")