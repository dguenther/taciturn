class Unit:
    def __init__(self):
        self.name = ''
        self.speed = 0
        self.ct = 0
        self.order_num = 0
        self.statuses = []
        self.slow_actions = []
        
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.ct = 0
        self.order_num = 0
        self.statuses = []
        self.slow_actions = []
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name