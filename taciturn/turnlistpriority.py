class TurnListPriority:

    def __init__(self, class_num, item_num):
        self.class_num = class_num
        self.item_num = item_num

    def __eq__(self, other):
        return (self.class_num == other.class_num and
            self.item_num == other.item_num)

    def __ne__(self, other):
        return (self.class_num != other.class_num or
            self.item_num != other.item_num)

    def __le__(self, other):
        if (self.class_num != other.class_num):
            return self.class_num <= other.class_num
        else:
            return self.item_num <= other.item_num

    def __ge__(self, other):
        if (self.class_num != other.class_num):
            return self.class_num >= other.class_num
        else:
            return self.item_num >= other.item_num

    def __lt__(self, other):
        if (self.class_num != other.class_num):
            return self.class_num < other.class_num
        else:
            return self.item_num < other.item_num

    def __gt__(self, other):
        if (self.class_num != other.class_num):
            return self.class_num > other.class_num
        else:
            return self.item_num > other.item_num
