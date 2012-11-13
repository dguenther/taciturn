class Unit:
    def __init__(self):
        self.name = ''
        self.speed = 0
        self.ct = 0
        self.order_num = 0
        self.statuses = []
        self.slow_action = None
        
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.ct = 0
        self.order_num = 0
        self.statuses = []
        self.slow_action = None
        
    def get_attributes(self):
        attributes = {}
        attributes['speed'] = self.speed
        attributes['ct'] = self.ct
        attributes['order_num'] = self.order_num
        return attributes
        
    def begin_casting(self, slow_action_template):
        self.slow_action = slow_action_template.evaluate_formula(self)
        return self.slow_action
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name