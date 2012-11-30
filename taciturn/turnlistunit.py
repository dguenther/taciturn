from turnlistpriority import TurnListPriority
from turnlistcomparable import TurnListComparable
from math import ceil


class TurnListUnit(TurnListComparable):
    def __init__(self, unit):
        self.unit = unit
        self.sim_ct = unit.ct
        self.ticks = 0

    def next_turn(self):
        next_turn = TurnListUnit(self.unit)
        next_turn.sim_ct = self.sim_ct
        next_turn.ticks = self.ticks
        next_turn.generate_tick()
        return next_turn

    def generate_tick(self):
        tick = int(ceil((100 - self.sim_ct) / self.unit.speed))
        self.ticks += tick
        self.sim_ct = self.sim_ct + tick * self.unit.speed - 100

    '''Inherited from TurnListComparable'''
    def ticks_remaining(self):
        return self.ticks

    '''Inherited from TurnListComparable'''
    def turn_priority(self):
        return TurnListPriority(2, self.unit.order_num)
