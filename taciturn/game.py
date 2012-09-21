from battle import Battle

class Game:

    def __init__(self):
        self.statuses = []
        self.slow_actions = []
        self.units = []
        
    def __init__(self, statuses, slow_actions, units):
        self.statuses = statuses
        self.slow_actions = slow_actions
        self.units = units
        
    def play(self):
        battle = Battle(self.units)
        battle.start()