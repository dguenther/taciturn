class SlowAction:
    def __init__(self):
        self.name = '';
        self.charge_ticks = 0
        self.caster = None
        
    def __init__(self, name, charge_ticks):
        self.name = name
        self.charge_ticks = charge_ticks
        self.caster = None 