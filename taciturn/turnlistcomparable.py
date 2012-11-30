class TurnListComparable:

    def ticks_remaining(self):
        raise NotImplementedError("ticks_remaining() was not implemented in a subclass of TurnListComparable.")

    def turn_priority(self):
        raise NotImplementedError("turn_priority() was not implemented in a subclass of TurnListComparable.")

    def __eq__(self, other):
        return (self.ticks_remaining() == other.ticks_remaining() and self.turn_priority() == other.turn_priority())

    def __ne__(self, other):
        return (self.ticks_remaining() != other.ticks_remaining() or self.turn_priority() != other.turn_priority())

    def __le__(self, other):
        if (self.ticks_remaining() != other.ticks_remaining()):
            return self.ticks_remaining() <= other.ticks_remaining()
        else:
            return self.turn_priority() <= other.turn_priority()

    def __ge__(self, other):
        if (self.ticks_remaining() != other.ticks_remaining()):
            return self.ticks_remaining() >= other.ticks_remaining()
        else:
            return self.turn_priority() >= other.turn_priority()

    def __lt__(self, other):
        if (self.ticks_remaining() != other.ticks_remaining()):
            return self.ticks_remaining() < other.ticks_remaining()
        else:
            return self.turn_priority() < other.turn_priority()

    def __gt__(self, other):
        if (self.ticks_remaining() != other.ticks_remaining()):
            return self.ticks_remaining() > other.ticks_remaining()
        else:
            return self.turn_priority() > other.turn_priority()
