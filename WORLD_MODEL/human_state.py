class HumanState:

    def __init__(self):

        self.energy=0.7
        self.stress=0.3
        self.resources=0.5
        self.social_support=0.4
        self.time_pressure=0.2

    def risk_tolerance(self):

        return (self.energy+self.resources)/2 - self.stress
