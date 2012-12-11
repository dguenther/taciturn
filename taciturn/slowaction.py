from turnlistitem import TurnListItem
from turnlistpriority import TurnListPriority


class SlowAction(TurnListItem):

    def __init__(self):
        self.name = ''
        self.formula = None
        self.charge_ticks = None
        self.caster = None

    def __init__(self, name, formula):
        self.name = name
        self.formula = None
        self.charge_ticks = None
        self.caster = None

    def evaluate_formula(self, caster):
        new_action = SlowAction()
        new_action.name = self.name
        new_action.charge_ticks = self.formula.evaluate(caster)
        return new_action

    def ticks_remaining(self):
        """Inherited from TurnListItem"""
        return self.charge_ticks

    def turn_priority(self):
        """Inherited from TurnListItem"""
        return TurnListPriority(0, 0)

    def next_turn(self):
        """Inherited from TurnListItem"""
        self.caster.slow_action = None

    def advance_ticks(self, ticks):
        """Inherited from TurnListItem"""
        self.charge_ticks -= ticks
