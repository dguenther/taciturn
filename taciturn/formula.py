'''
Definition
----------
Supported formulas are:
<operand> <operator> <operand>
<operand>

* Operands can be either unit attributes or numbers.
* Unit attributes are not case sensitive.

Here are a few examples:
50 / Speed
3
'''
class Formula:
    def __init__(self):
        self.formula = ''
        
    def __init__(self, formula):
        self.formula = formula
        
    def evaluate(self, caster):
        tokens = formula.split()
        token_count = len(tokens)
        if (token_count == 1):
            result = parse_operand(tokens[0], caster)
        return None
        
    def parse_operand(self, operand, caster):
        try:
            # see if the operand is a number
            value = float(operand)
            return value
        except ValueError:
            # if it's not a number, see if it's a unit attribute
            normalized_operand = operand.lower()
            for key, value in iteritems(caster.get_attributes()):
                if key == normalized_operand:
                    return value
            raise Exception('Operand %s not in Unit' % (operand))
        return None