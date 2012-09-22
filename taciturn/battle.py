from unit import Unit
from status import Status
from slowaction import SlowAction
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
from math import ceil

class Battle:

    def __init__(self):
        self.units = []
        self.clocktick = 1
        self.slow_action_order = defaultdict(list)
        
    def __init__(self, units):
        self.units = units
        self.clocktick = 1
        self.slow_action_order = defaultdict(list)
        
    def setup_ct(self):
        for unit in self.units:
            unit.ct = 50
            
    def tick_clock(self):
        self.status_phase()
        self.slow_action_phase()
        self.active_turn_phase()
        
    def status_phase(self):
        for unit in self.units:
            delete_statuses = []
            for status in unit.statuses:
                status.duration -= 1
                if status.duration == 0:
                    # keep track of statuses to be removed
                    delete_statuses.append(status)
            # remove statuses from unit
            for status in delete_statuses:
                unit.statuses.remove(status)
        
    def slow_action_phase(self):
        for key in sorted(self.slow_action_order.keys()):
            if key == 1:
                while len(self.slow_action_order[1]) > 0:
                    action = self.slow_action_order[1].pop()
                    # execute action
                # remove the key
                del self.slow_action_order[1]
                # TODO: add/remove slow actions from units
            else:
                # decrease clocktick
                self.slow_action_order[key-1] = self.slow_action_order[key]
                # remove the key
                del self.slow_action_order[key]
                
    def generate_turn_list(self):
        # generate unit queue
        unit_order = defaultdict(list)
        for unit in self.units:
            tick = int(ceil((100 - unit.ct) / unit.speed))
            unit_order[tick].append(unit)
        # sort each queue bucket by order number
        for unit_list in unit_order.itervalues():
            unit_list.sort(key=lambda x : x.order_num)
        # merge slow action order and unit queue
        turn_list = deepcopy(self.slow_action_order)
        for key,value in unit_order.iteritems():
            turn_list[key].extend(value)
        return turn_list
        
    def generate_turn_list2(self):
        # unit tuple: (virtual_ct, tick, unit)
        # set up queue of tuples:
        # ( generate ticks, set up virtual_ct )
        # sort the queue by ticks, then order number if ticks are equal
        # set up slow action queue
        # while turn_list < 20:
        # pull minimum tick from (slow action queue, unit queue)
        # if from unit queue, update tick and ct and re-sort
        
        
    def active_turn_phase(self):
        for unit in units:
            unit.ct += unit.speed
        
    def start(self):
        self.setup_ct()
        pprint(dict(self.generate_turn_list()))
        #while True:
        #    self.tick_clock()