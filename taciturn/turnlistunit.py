from turnlistpriority import TurnListPriority
from turnlistitem import TurnListItem
from math import ceil


class TurnListUnit(TurnListItem):

    def __init__(self, unit):
        self.unit = unit
        self.sim_ct = unit.ct
        self.ticks = 0

    def generate_tick(self):
        tick = int(ceil((100 - float(self.sim_ct)) / self.unit.speed))
        self.ticks += tick
        self.sim_ct = self.sim_ct + tick * self.unit.speed - 100

    def next_turn(self):
        """Inherited from TurnListItem"""
        self.unit.ct = self.sim_ct

    def advance_ticks(self, ticks):
        """Inherited from TurnListItem"""
        self.unit.ct += ticks * self.unit.speed

    def ticks_remaining(self):
        """Inherited from TurnListItem"""
        return self.ticks

    def turn_priority(self):
        """Inherited from TurnListItem"""
        return TurnListPriority(2, self.unit.order_num)
