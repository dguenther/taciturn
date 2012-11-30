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

    def generate_status_list(self):
        list = []
        for unit in self.units:
            for status in unit.statuses:
                list.append(status)
        return list

    def generate_slow_action_list(self):
        list = []
        for unit in self.units:
            if (unit.slow_action):
                list.append(unit.slow_action)
        return list

    def generate_unit_list(self):
        list = []
        for unit in self.units:
            new_unit = TurnListUnit(unit)
            new_unit.generate_tick()
            list.append(new_unit)
        return list

    def generate_display_list(self, list_length):
        status_list = self.generate_status_list()
        slow_action_list = self.generate_slow_action_list()
        unit_list = self.generate_unit_list()
        heap = []
        display_list = []

        # set up heap
        for item in status_list:
            heapq.heappush(heap, item)
        for item in slow_action_list:
            heapq.heappush(heap, item)
        for item in unit_list:
            heapq.heappush(heap, item)

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

    def start(self):
        self.setup()
        #self.generate_display_list()
        pprint(self.generate_display_list(40))
