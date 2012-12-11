from turnlistunit import TurnListUnit
from pprint import pprint
import heapq


class Battle:

    def __init__(self):
        self.campaign = None
        self.units = []
        self.clocktick = 1
        self.turn_order = []

    def __init__(self, campaign, units):
        self.campaign = campaign
        self.units = units
        self.clocktick = 1
        self.turn_order = []

    def setup(self):
        for unit in self.units:
            # default ct is 50
            unit.ct = 50

    def make_status_list(self):
        list = []
        for unit in self.units:
            for status in unit.statuses:
                list.append(status)
        return list

    def make_slow_action_list(self):
        list = []
        for unit in self.units:
            if (unit.slow_action):
                list.append(unit.slow_action)
        return list

    def make_unit_list(self):
        list = []
        for unit in self.units:
            new_unit = TurnListUnit(unit)
            new_unit.generate_tick()
            list.append(new_unit)
        return list

    def make_turn_order_heap(self):
        status_list = self.make_status_list()
        slow_action_list = self.make_slow_action_list()
        unit_list = self.make_unit_list()
        heap = []

        # set up heap
        for item in status_list:
            heapq.heappush(heap, item)
        for item in slow_action_list:
            heapq.heappush(heap, item)
        for item in unit_list:
            heapq.heappush(heap, item)
        return heap

    def make_display_list(self, list_length):
        heap = self.make_turn_order_heap()
        display_list = []

        # pull from heap to make the list
        while list_length > 0:
            current_item = heapq.heappop(heap)
            try:
                # make special allowances for units
                current_item.generate_tick()
                heapq.heappush(heap, current_item)
                current_item = current_item.unit
            except AttributeError:
                # current_item isn't a unit, so don't do anything different
                pass
            display_list.append(current_item)
            list_length -= 1
        return display_list

    def next_turn(self):
        heap = self.make_turn_order_heap()
        active_item = heapq.heappop(heap)
        ticks = active_item.ticks_remaining()
        active_item.next_turn()
        for item in heap:
            item.advance_ticks(ticks)

    def start(self):
        self.setup()
        #self.make_display_list()
        pprint(self.make_display_list(40))
