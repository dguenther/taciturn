from turnlistcomparable import TurnListComparable
from turnlistpriority import TurnListPriority


class Status(TurnListComparable):

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    '''Inherited from TurnListComparable'''
    def ticks_remaining(self):
        return self.duration

    '''Inherited from TurnListComparable'''
    def turn_priority(self):
        return TurnListPriority(0, 0)
