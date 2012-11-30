from turnlistcomparable import TurnListComparable
from turnlistpriority import TurnListPriority


class SlowAction(TurnListComparable):
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

    '''Inherited from TurnListComparable'''
    def ticks_remaining(self):
        return self.charge_ticks

    '''Inherited from TurnListComparable'''
    def turn_priority(self):
        return TurnListPriority(0, 0)
