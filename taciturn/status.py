from turnlistitem import TurnListItem
from turnlistpriority import TurnListPriority


class Status(TurnListItem):

    def __init__(self, name, duration, unit):
        self.name = name
        self.duration = duration
        self.affected_unit = unit

    def ticks_remaining(self):
        """Inherited from TurnListItem"""
        return self.duration

    def turn_priority(self):
        """Inherited from TurnListItem"""
        return TurnListPriority(0, 0)

    def next_turn(self):
        self.affected_unit.statuses.remove(self)

    def advance_ticks(self, ticks):
        self.duration -= ticks
