class SlowAction:
    def __init__(self):
        self.name = '';
		self.formula = None
        self.charge_ticks = None
        self.caster = None
        
    def __init__(self, name, formula):
        self.name = name
		self.formula = None
        self.charge_ticks = None
        self.caster = None 
		
	def evaluate_formula(self, caster):
		new_action = SlowAction()
		new_action.name = self.name
		new_action.charge_ticks = self.formula.evaluate(caster)
		return new_action