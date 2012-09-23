from unit import Unit
from status import Status
from slowaction import SlowAction
from collections import defaultdict
from copy import deepcopy, copy
from pprint import pprint
from math import ceil

class Battle:

    def __init__(self):
        self.units = []
        self.clocktick = 1
        self.turn_order = []
        
    def __init__(self, units):
        self.units = units
        self.clocktick = 1
        self.turn_order = []
        
    def setup(self):
        for unit in self.units:
            unit.ct = 50
            self.turn_order.append((self.next_turn_tick(unit).next(), unit))
            self.turn_order.sort(cmp=self.turn_order_compare)
            
    def tick_clock(self):
        # goto next thing in turn_order
        pass
        
    def generate_display_list(self):
        order_display = copy(self.turn_order)
        # while order_display isn't full
        #   count through items in order_display
        #   if item is a unit
        #       add unit's next active turn into order_display and sort
        idx = 0
        unit_gens = {}
        while idx < 40:
            item = order_display[idx][1]
            if isinstance(item, Unit):
                if item not in unit_gens:
                    unit_gens[item] = self.next_turn_tick(item)
                    # get rid of unit's next turn (which is already
                    # included from the turn_order list that was copied)
                    unit_gens[item].next()
                
                t = unit_gens[item].next()

                # slice the array to sort smaller portion
                # for performance reasons at small (<10k) list sizes
                order_display.append((t, item))
                to_sort = order_display[idx:]
                to_sort.sort(cmp=self.turn_order_compare)
                order_display = order_display[:idx] + to_sort
            idx += 1
        return order_display

    def turn_order_compare(self, x, y):
        if x[0] != y[0]:
            return cmp(x[0], y[0])
        else:
            x = x[1]
            y = y[1]
            # if x is a Status, it should come first regardless
            # (order of two Statuses ending doesn't matter)
            if isinstance(x, Status):
                return -1
            # otherwise y should come first (x wasn't a Status)
            elif isinstance(y, Status):
                return 1
            # if neither were Statuses
            elif isinstance(x, SlowAction):
                # if both were SlowActions, whichever comes first in the battle's
                # turn_order list should be first (the casting order is implicit
                # in the order of the SlowActions in the turn_order list)
                if isinstance(y, SlowAction):
                    return cmp(self.turn_order.indexof(x), self.turn_order.indexof(y))
                # otherwise x is a SlowAction and y is a Unit so x comes first
                else:
                    return -1
            # otherwise, x is a Unit and y is a SlowAction so y comes first
            elif isinstance(y, SlowAction):
                return 1
            # otherwise both are Units and order is determined by their
            # order_num for this battle
            elif isinstance(x, Unit) and isinstance(y, Unit):
                return cmp(x.order_num, y.order_num)
            else:
                assert False
        
    def next_turn_tick(self, unit):
        ct = unit.ct
        last_tick = 0
        while True:
            tick = int(ceil((100 - ct) / unit.speed))
            yield last_tick + tick
            last_tick += tick
            ct = ct + tick * unit.speed - 100
        
    def start(self):
        self.setup()
        #self.generate_display_list()
        pprint(self.generate_display_list())
        #while True:
        #    self.tick_clock()