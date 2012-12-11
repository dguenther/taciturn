class TurnListItem:

    def ticks_remaining(self):
        """Return the number of ticks until the next turn."""
        raise NotImplementedError("ticks_remaining() was not implemented in a subclass of TurnListItem.")

    def turn_priority(self):
        """Return an instance of TurnListPriority that dictates what priority one TurnListItem should
        have over another.

        """
        raise NotImplementedError("turn_priority() was not implemented in a subclass of TurnListItem.")

    def advance_ticks(self, ticks):
        """Advance an item by a given number of ticks."""
        raise NotImplementedError("advance_ticks() was not implemented in a subclass of TurnListItem.")

    def next_turn(self):
        """Perform actions that clean up an item after its active turn."""
        raise NotImplementedError("next_turn() was not implemented in a subclass of TurnListItem.")

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
